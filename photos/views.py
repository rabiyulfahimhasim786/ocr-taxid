from django.shortcuts import render, redirect
from .models import Category, Photo, Csv, Key, Tables
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
import requests
# Create your views here.
from django.http import HttpResponse, JsonResponse
import pandas as pd
import json
import time
#AWS s3
import boto3
import os
from functools import reduce
#import boto3
# ACCESS_KEY = "Accesskey"
# SECRET_KEY = "secretkey"

from botocore.exceptions import ClientError
import datetime
#create your views here

def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('gallery')

    return render(request, 'photos/login_register.html', {'page': page})


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('gallery')

    context = {'form': form, 'page': page}
    return render(request, 'photos/login_register.html', context)


@login_required(login_url='login')
def gallery(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.filter(category__user=user)
    else:
        photos = Photo.objects.filter(
            category__name=category, category__user=user)

    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)


def Convert(string):
	li = list(string.split(","))
	return li

@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    csv = Csv.objects.get(id=pk)
    key = Key.objects.get(id=pk)
    tables = Tables.objects.get(id=pk)
    print(csv.csvfile)
    print(key.keyfile)
    print(tables.tablefile)
    df = pd.read_csv(csv.csvfile, header= 0, encoding= 'unicode_escape')
    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    print(data)
    keydf = pd.read_csv(key.keyfile, header= 0, encoding= 'unicode_escape')
    # parsing the DataFrame in json format.
    key_json_records = keydf.reset_index().to_json(orient ='records')
    keydata = []
    keydata = json.loads(key_json_records)
    print(keydata)
	#context = {'d': data}
    #fruits = ['https://raw.githubusercontent.com/cs109/2014_data/master/countries.csv', 'https://raw.githubusercontent.com/cs109/2014_data/master/countries.csv']
    #fruits = tables.tablefile
    bad_chars = ['[', ']', "'", "'"]
    tables_string = ''.join((filter(lambda i: i not in bad_chars,
							tables.tablefile)))
    print(tables_string)
    tableli = Convert(str(tables_string))
    print(tableli)
    #one data frame to html conversion
    #tablesdf = pd.read_csv(tables_string)
    #tablesobject = tablesdf.to_html()
    tablesdf = pd.read_csv(tableli[0], header= 0, encoding= 'unicode_escape')
    tablesobject = tablesdf.to_html()
    #multi data frame to html conversion
    #tablevalue = []
    #for tablestable in tableli:
    #    print(tablestable)
    #    tablesdf = pd.read_csv(tablestable)
    #    tablesobject = tablesdf.to_html()
    #    tablevalue.append(tablesobject)
    #print(tablevalue)
	#return render(request, 'table.html', context)
    #meging csv files
    #filesnames = ['file1.csv', 'file2.csv']
    #ui =[]
    #for filename in filesnames:
    #    tdf = pd.read_csv(filename, index_col=None, header=0)
     #   ui.append(tdf)
    #df = pd.read_csv()
    #print(ui)
    #df1 = pd.concat(pd.read_csv(), axis=0, ignore_index=True)
    #geeks = df1.to_html()
    #tabledf = pd.concat(map(pd.read_csv, tableli), ignore_index=True)
    #geeks = tabledf.to_html()
    # df_append = pd.DataFrame()#append all files together
    # for file in tableli:
    #         df_temp = pd.read_csv(file)
    #         df_append = df_append.append(df_temp, ignore_index=True)
    # tablesobject = df_append#.to_html
    text = {'photo': photo, 'd': data, 'keydata':keydata, 'tabledata':tablesobject }#'tabledata': tablesobject}
    return render(request, 'photos/photo.html', text)#{'photo': photo})


@login_required(login_url='login')
def addPhoto(request):
    user = request.user

    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
            )
        time.sleep(18)
        #x = requests.get('http://127.0.0.1:8000/text/')
        #AWS s3 file post
        # ACCESS_KEY = "Accesskey"
        # SECRET_KEY = "secretkey"
        # overall text links
        ACCESS_KEY = "Accesskey"
        SECRET_KEY = "secretkey"
        s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        response = s3_client.list_objects_v2(Bucket='bucketname', Prefix='foldername')
        all = response['Contents']        
        latest = max(all, key=lambda x: x['LastModified'])
        print(latest)
        #print(latest.values())
        list(reduce(lambda x, y: x + y, latest.items()))
        a = list(reduce(lambda x, y: x + y, latest.items()))
        print(a[1])
        #file downloading 
        #print(latest.values())
        list(reduce(lambda x, y: x + y, latest.items()))
        a = list(reduce(lambda x, y: x + y, latest.items()))
        #print(a[1])
        urllink = a[1]
        url = f"https://bucketname.s3.amazonaws.com/{urllink}"
        member = Csv(csvfile=url)
        member.save()
        #key value url links to download
        key_s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        keyresponse = key_s3_client.list_objects_v2(Bucket='bucketname', Prefix='foldername')
        keyall = keyresponse['Contents']        
        keylatest = max(keyall, key=lambda x: x['LastModified'])
        print(keylatest)
        #print(latest.values())
        list(reduce(lambda x, y: x + y, keylatest.items()))
        keya = list(reduce(lambda x, y: x + y, keylatest.items()))
        print(keya[1])
        #file downloading 
        #print(latest.values())
        list(reduce(lambda x, y: x + y, keylatest.items()))
        keya = list(reduce(lambda x, y: x + y, keylatest.items()))
        #print(a[1])
        keyurllink = keya[1]
        keyurl = f"https://bucketname.s3.amazonaws.com/{keyurllink}"
        print(keyurl)
        #datas = {"key": url}
        keymember = Key(keyfile=keyurl)
        keymember.save()
        #tables url links to download
        s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        response = s3_client.list_objects_v2(Bucket='bucketname', Prefix='foldername')
        all = response['Contents']        
        latest = max(all, key=lambda x: x['LastModified'])
        #print(latest)
        #print(latest.values())
        list(reduce(lambda x, y: x + y, latest.items()))
        a = list(reduce(lambda x, y: x + y, latest.items()))
        #print(a[1])

        #file downloading 
        #print(latest.values())
        list(reduce(lambda x, y: x + y, latest.items()))
        a = list(reduce(lambda x, y: x + y, latest.items()))
        #print(a[1])
        urllink = a[1]
        testurl = urllink[0:72]
        print(testurl)
        prefix = testurl
        #prefix = "tables/3b983c8d07fcf5de103bc43711b526d20be7aa800e4f5627d8e7acafe788863d/"
        s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)#)
        bucket = s3.Bucket(name="bucketname")
        filtered_file_names =[]
        FilesNotFound = True
        for obj in bucket.objects.filter(Prefix=prefix):
            #print('{0}:{1}'.format(bucket.name, obj.key))
            #full_s3_file = '{0}/{1}'.format(bucket.name, obj.key)
            #filtered_file_names.append('{0}/{1}'.format(bucket.name, obj.key))
            filtered_file_names.append('https://{0}.s3.amazonaws.com/{1}'.format(bucket.name, obj.key))
            #https://{0}.s3.amazonaws.com/{1}
            #print(filtered_file_names)
            FilesNotFound = False
        print(filtered_file_names)
        if FilesNotFound:
            print("ALERT", "No file in {0}/{1}".format(bucket, prefix))
        tablemember = Tables(tablefile=filtered_file_names)
        tablemember.save()
        return redirect('gallery')
    context = {'categories': categories}
    return render(request, 'photos/add.html', context)


  
def index(request):
    return HttpResponse("Hello, world.")


def text_views(request):
    #ACCESS_KEY = "Accesskey"
    #SECRET_KEY = "secretkey"
    
    ACCESS_KEY = "Accesskey"
    SECRET_KEY = "secretkey"
    s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    response = s3_client.list_objects_v2(Bucket='bucketname', Prefix='foldername')
    all = response['Contents']        
    latest = max(all, key=lambda x: x['LastModified'])
    print(latest)
    #print(latest.values())
    list(reduce(lambda x, y: x + y, latest.items()))
    a = list(reduce(lambda x, y: x + y, latest.items()))
    print(a[1])

    #file downloading 
    #print(latest.values())
    list(reduce(lambda x, y: x + y, latest.items()))
    a = list(reduce(lambda x, y: x + y, latest.items()))
    #print(a[1])
    urllink = a[1]
    url = f"https://bucketname.s3.amazonaws.com/{urllink}"
    print(url)
    datas = {"key": url}
    #member = Csv(csvfile=url)
    #member.save()
    return JsonResponse({"code": "1", "status": "200", "data": [datas]})



def deleteItem(request, id):
    item = Photo.objects.get(id=id)
    item.delete()
    file = Csv.objects.get(id=id)
    file.delete()
    keyfile = Key.objects.get(id=id)
    keyfile.delete()
    tablefile = Tables.objects.get(id=id)
    tablefile.delete()
    return redirect('gallery')
