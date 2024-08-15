from django.urls import path
from . import views

# app_name = 'adminsite'

urlpatterns = [
    # SportType URLs
    path('sporttypes/', views.sporttype_list, name='sporttype_list'),
    path('sporttypes/create/', views.sporttype_create, name='sporttype_create'),
    path('sporttypes/update/<int:pk>/', views.sporttype_update, name='sporttype_update'),
    path('sporttypes/delete/<int:pk>/', views.sporttype_delete, name='sporttype_delete'),

    # Team URLs
    path('teams/', views.team_list, name='team_list'),
    path('teams/create/', views.team_create, name='team_create'),
    path('teams/update/<int:pk>/', views.team_update, name='team_update'),
    path('teams/delete/<int:pk>/', views.team_delete, name='team_delete'),

    # Player URLs
    path('players/', views.player_list, name='player_list'),
    path('players/create/', views.player_create, name='player_create'),
    path('players/update/<int:pk>/', views.player_update, name='player_update'),
    path('players/delete/<int:pk>/', views.player_delete, name='player_delete'),
    path('players/bulk_add/', views.bulk_add_players, name='bulk_add_players'),

    # Event URLs
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/update/<int:pk>/', views.event_update, name='event_update'),
    path('events/delete/<int:pk>/', views.event_delete, name='event_delete'),

     # Bet URLs
    path('bets/', views.bet_list, name='bet_list'),
    path('bets/create/', views.bet_create, name='bet_create'),
    path('bets/update/<int:pk>/', views.bet_update, name='bet_update'),
    path('bets/delete/<int:pk>/', views.bet_delete, name='bet_delete'),

    #Venue
    path('venuelist', views.venue_list, name='venue_list'),
    path('venue/<int:pk>/', views.venue_detail, name='venue_detail'),
    path('venue/new/', views.venue_create, name='venue_create'),
    path('venue/<int:pk>/edit/', views.venue_update, name='venue_update'),
    path('venue/<int:pk>/delete/', views.venue_delete, name='venue_delete'),
    path('venue/bulk_add/', views.bulk_add_venues, name='bulk_add_venues'),


]
