from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import slugify
from .models import Category, Product, SubCategory

'''# Unregister first if already registered
if admin.site.is_registered(Product):
    admin.site.unregister(Product)
if admin.site.is_registered(Category):
    admin.site.unregister(Category)'''

# ——— Safely unregister if already registered ———
for model in (Product, Category):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass


# ——— Category ———
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'preview')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    # show the image thumbnail in list display
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="40" height="40" style="object-fit:cover;">', obj.image.url)
        return "-"
    preview.short_description = "Image"

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "slug")
    list_filter = ("category",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


# ——— Product ———
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_featured', 'thumb')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)

    # small image preview
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;">', obj.image.url)
        return "-"
    thumb.short_description = "Image"
    '''fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'category', 'description')
        }),
        ('Pricing', {
            'fields': ('price',)
        }),
        ('Inventory', {
            'fields': ('stock', 'is_featured')
        }),
        ('Media', {
            'fields': ('image',)
        })
    )'''
