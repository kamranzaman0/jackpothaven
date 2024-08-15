from django.urls import path, include
from adminsite import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    path('check-user-exists/', views.check_user_exists, name='check_user_exists'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='adminsite/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='adminsite/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='adminsite/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='adminsite/password_reset_complete.html'), name='password_reset_complete'),



    path('checkout/<int:id>/', views.checkout, name='checkout'),
    path('webhook/', views.webhook, name='stripe-webhook'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),

    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/change-role/', views.change_user_role, name='change_user_role'),
    path('profile/', views.user_profile_list, name='user_profile_list'),


]