from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('customer_dashboard/',views.customer_dashboard,name='customer_dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('logout/', views.user_logout, name='logout'),
    path('edit_customer/', views.edit_customer, name='edit_customer'),
    path('list/', views.AddressListView.as_view(), name='address_list'),
    path('add/', views.AddressCreateView.as_view(), name='address_add'),
    path('<int:pk>/edit/', views.AddressUpdateView.as_view(), name='address_edit'),
    path('address/<int:pk>/delete/', views.AddressDeleteView.as_view(), name='address_delete'),

]