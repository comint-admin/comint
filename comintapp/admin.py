from django.contrib import admin

from comintapp.models import ComintUser

# Register your models here.
class ComintUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')

admin.site.register(ComintUser, ComintUserAdmin)