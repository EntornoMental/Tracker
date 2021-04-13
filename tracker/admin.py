from django.contrib import admin
from .models import User, Time, File
# Register your models here.

admin.site.register(User)
admin.site.register(Time)
admin.site.register(File)