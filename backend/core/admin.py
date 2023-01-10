from django.contrib import admin
from .models import Category, Annotation, Like, Favorite, Report
# Register your models here.



admin.site.register(Category)
admin.site.register(Annotation)
admin.site.register(Like)
admin.site.register(Favorite)
admin.site.register(Report)