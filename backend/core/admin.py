from django.contrib import admin
from .models import User, Category, Annotation, Like
# Register your models here.


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Annotation)
admin.site.register(Like)