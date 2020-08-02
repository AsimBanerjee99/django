from django.contrib import admin
from .models import rowName, columnName, timeTable


# Register your models here.
admin.site.register(rowName)
admin.site.register(columnName)
admin.site.register(timeTable)


