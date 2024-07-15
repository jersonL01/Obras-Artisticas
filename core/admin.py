from django.contrib import admin
from .models import *
from django.contrib.admin import ModelAdmin
from admin_confirm import AdminConfirmMixin
# Register your models here.

class ObrasAdmin(admin.ModelAdmin):
    list_display = ['nombre','precio','stock','descripcion','historia', 'imagen', 'tecnica']
    search_fields = ['nombre']
    list_per_page = 10

class ObrasAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['nombre','precio','stock','descripcion','historia', 'imagen', 'tecnica']



admin.site.register(TipoObras)
admin.site.register(Producto, ObrasAdmin)