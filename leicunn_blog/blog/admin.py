from django.contrib import admin
from .models import *


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Opinion)
admin.site.register(Comment)