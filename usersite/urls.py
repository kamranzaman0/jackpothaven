from django.contrib import admin
from django.urls import path, include
from usersite import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('aboutus/', views.about_us, name='aboutus'),
    path('contactus/', views.contact_us, name='contactus'),
    path('allevents/', views.all_events, name='allevents'),

    # path('showallevents/', views.showallevents, name='showallevents'),
    path('detail_of_event/<int:id>/', views.detail_of_event, name='detail_of_event'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
