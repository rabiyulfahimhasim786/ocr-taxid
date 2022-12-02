from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.Photo.delete()      
        super().delete(*args, **kwargs)


# class Photo(models.Model):
#     class Meta:
#         verbose_name = 'Photo'
#         verbose_name_plural = 'Photos'
    
#     category = models.ForeignKey(
#         Category, on_delete=models.SET_NULL, null=True, blank=True)
#     image = models.ImageField(null=False, blank=False)
#     description = models.TextField()

#     def __str__(self):
#         return self.description
# 


class Photo(models.Model):
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.FileField(null=False, blank=False,  upload_to='async-kv-table')
    description = models.TextField()

    def __str__(self):
        return self.description
# # 
class Csv(models.Model):
    class Meta:
        verbose_name = 'Csv'
        verbose_name_plural = 'Csvs'
    category = models.ForeignKey(
         Category, on_delete=models.SET_NULL, null=True, blank=True)
    #csvphoto =  models.OneToOneField(Photo, on_delete=models.SET_NULL)
    id = models.AutoField(primary_key=True)
    csvfile = models.URLField(null=False, blank=False,)
    

    def __str__(self):
        return self.csvfile

class Key(models.Model):
    class Meta:
        verbose_name = 'Key'
        verbose_name_plural = 'Keys'
    category = models.ForeignKey(
         Category, on_delete=models.SET_NULL, null=True, blank=True)
    #csvphoto =  models.OneToOneField(Photo, on_delete=models.SET_NULL)
    id = models.AutoField(primary_key=True)
    keyfile = models.URLField(null=False, blank=False,)
    

    def __str__(self):
        return self.keyfile

class Tables(models.Model):
    class Meta:
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'
    category = models.ForeignKey(
         Category, on_delete=models.SET_NULL, null=True, blank=True)
    #csvphoto =  models.OneToOneField(Photo, on_delete=models.SET_NULL)
    id = models.AutoField(primary_key=True)
    tablefile = models.URLField(null=False, blank=False,)
    

    def __str__(self):
        return self.tablefile