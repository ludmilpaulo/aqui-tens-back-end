from django.contrib import admin
from .models import ShopCategory, Shop

@admin.register(ShopCategory)
class ShopCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass
