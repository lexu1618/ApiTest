from django.contrib import admin
from .models import *

# Register your models here.

# 在后台注册ORM，参数为类名
admin.site.register(DB_tucao)
admin.site.register(DB_home_href)
admin.site.register(DB_project)
admin.site.register(DB_apis)