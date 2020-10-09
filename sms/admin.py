from django.contrib import admin
from .models import *
# Register your models here.

class StockAdmin(admin.ModelAdmin):
   list_display = ['category', 'item_name', 'quantity']
   list_filter = ['category']
   search_fields = ['category', 'item_name']

class IssueAdmin(admin.ModelAdmin):
   list_display = ['stock', 'issue_quantity', 'issue_to']
   list_filter = ['stock', 'issue_to']
   search_fields = ['stock', 'issue_to']

class ReceiveAdmin(admin.ModelAdmin):
   list_display = ['stock', 'receive_quantity', 'receive_from']
   list_filter = ['stock', 'receive_from']
   search_fields = ['stock', 'receive_from']


admin.site.register(Stock,StockAdmin)
admin.site.register(Category)
admin.site.register(Issue,IssueAdmin)
admin.site.register(Receive,ReceiveAdmin)