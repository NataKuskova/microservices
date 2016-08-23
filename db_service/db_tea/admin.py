from django.contrib import admin
from db_tea.models import *


class ListOfOrderInline(admin.TabularInline):
    model = ListOfOrder
    extra = 1
    raw_id_fields = ("product",)


class OrderAdmin(admin.ModelAdmin):
    inlines = (ListOfOrderInline,)
    list_display = ['id', 'user', 'sum', 'date_order']
    list_display_links = ('id', 'user')
    date_hierarchy = 'date_order'
    list_filter = ('date_order',)
    list_per_page = 10
    search_fields = ('user__name', 'user__surname', 'sum',)


class ProductAdmin(admin.ModelAdmin):
    inlines = (ListOfOrderInline,)
    list_display = ['id', 'name', 'category', 'price', 'quantity', 'photo',
                    'user']
    list_display_links = ('id', 'name')
    list_filter = ('category', 'user',)
    search_fields = ('name', 'price', 'quantity', 'category__name')
    list_per_page = 10


class BuyerAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'email']
    list_display_links = ('name', 'surname')
    fields = (('name', 'surname'), 'email', 'address', 'phone')
    list_per_page = 10
    search_fields = ('name', 'surname', 'email', 'phone', 'address',)


admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Buyer, BuyerAdmin)
