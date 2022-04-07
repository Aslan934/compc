from django.contrib import admin
from shop import models


class ProductSpecificationInline(admin.TabularInline):
    model = models.ProductSpecification


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductSpecificationInline]


class ProductImageInline(admin.StackedInline):
    model = models.ProductImage


class ProductSpecificationValueInline(admin.StackedInline):
    model = models.ProductSpecificationValue


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline, ProductSpecificationValueInline
    ]
    list_filter = ('category',)
    list_display = ('title', 'get_model', 'price', 'created_at')
    search_fields = ['title']

    def get_model(self, obj):
        return models.ProductSpecificationValue.objects.get(specification__name__contains='model', product=obj)
    get_model.short_description = 'Model'


admin.site.register(models.Banner)
