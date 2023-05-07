from django.contrib import admin
from .models import User, Message, Profile
from .models import Code

# Register your models here.

admin.site.register(User)
admin.site.register(Message)
admin.site.register(Profile)
admin.site.register(Code)