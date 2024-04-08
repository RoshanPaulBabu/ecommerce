from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
     path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),
]