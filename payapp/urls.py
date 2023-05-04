from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('send-money/', views.send_money, name='send-money'),
    path('request-money/', views.request_money, name='request-money'),
    path('requests/', views.requests, name='requests'),
    path('approve-request/', views.approve_request, name='approve-request'),
    path('deny-request/', views.deny_request, name='deny-request'),
    path('notifications/', views.notifications, name='notifications'),
    path('',views.index_admin,name='dashboard-admin'),
    path('add-admin/', views.add_admin, name='add-admin'),
    path('all-users/', views.all_users, name='all-users'),
    path('all-transactions/', views.all_transactions, name='all-transactions')
]
