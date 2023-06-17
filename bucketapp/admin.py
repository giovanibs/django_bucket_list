from django.contrib import admin  
from .models import Bucket, Task

# Register your models here.
admin.site.register(Bucket)
admin.site.register(Task)
