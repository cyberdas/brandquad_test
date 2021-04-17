from django.contrib import admin

#from .models import Log

class LogAdmin(admin.ModelAdmin):
    pass
    # list_display = [field.name for field in Log._meta.get_fields()]
    # search_fields
    # list_filter

#admin.site.register(Log, LogAdmin)
