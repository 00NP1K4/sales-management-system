from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = 'index'),
    path('stocks_list/', stocks, name = 'stock'),
    path('stock_detail/<str:pk>/', detail, name = 'detail'),
    path('add/', add_items, name='add'),
    path('update/<str:pk>', update_items, name = 'update'),
    path('delete/<str:pk>/', delete_items, name= 'delete'),
    path('issue/<str:pk>/', issue_items, name="issue"),
    path('receive/<str:pk>/', receive_items, name="receive"),
    path('receivesummary/', receive_summary, name="receivesummary"),
    path('issuesummary/', issue_summary, name="issuesummary"),
    path('signin/', signin, name='signin'),
]