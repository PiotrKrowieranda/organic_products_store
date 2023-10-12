from django.contrib import admin
from .models import Ingredient, Category, Product

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'vat', 'stock', 'image')
    list_filter = ('categories', 'ingredients')
    search_fields = ('name', 'description')

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)