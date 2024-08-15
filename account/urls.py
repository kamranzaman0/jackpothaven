from django.urls import path
from account import views


urlpatterns = [
    path('dashboard', views.user_dashboard, name='user_dashboard'),
    path('profile/', views.user_profile, name='user_profile'),
    path('bettinghistory/', views.user_betting_history, name='user_betting_history'),
    path('balance/', views.user_balance, name='user_balance'),
    path('verify-phone-number/', views.verify_phone_number, name='verify_phone_number'),



    # path('send-otp/', views.send_otp, name='send_otp'),
    # path('success/', views.success, name='success_otp'),  # Create a success view

]