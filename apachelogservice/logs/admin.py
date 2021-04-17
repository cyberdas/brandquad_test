from django.contrib import admin

from .models import Log


class LogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Log._meta.get_fields()]
    search_fields = ('ip_address', 'timestamp', 'http_method', 'response_status_code')
    list_filter = ('ip_address', 'timestamp', 'http_method', 'response_status_code')


admin.site.register(Log, LogAdmin)
