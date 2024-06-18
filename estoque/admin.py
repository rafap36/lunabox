from django.contrib import admin
from .models import Localidade, Item
# Register your models here.


admin.site.register(Localidade)
admin.site.register(Item)


admin.site.site_header = 'D-LUNA'
admin.site.index_title = 'Painel de Administração'
admin.site.site_title = 'DLUNA Admin'
