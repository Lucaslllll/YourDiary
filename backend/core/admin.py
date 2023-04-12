from django.contrib import admin
from .models import Category, Annotation, Like, Favorite, Report
from .models import AnnotationImage
# Register your models here.



admin.site.register(Category)
admin.site.register(Annotation)
admin.site.register(Like)
admin.site.register(Favorite)
admin.site.register(Report)
admin.site.register(AnnotationImage)