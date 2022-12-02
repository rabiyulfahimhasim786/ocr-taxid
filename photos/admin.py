from django.contrib import admin

# Register your models here.

from .models import Photo, Category, Csv, Key

admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(Csv)
admin.site.register(Key)
