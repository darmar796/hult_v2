from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.main, name='main'),
    # path('members/', views.members, name='members'),
    # path('members/details/<int:id>', views.details, name='details'),
    path('testing/', views.testing, name='testing'),
    path('about/', views.about, name='about'),
    path('add_reservation/', views.add_reservation, name='add_reservation'),
    path('input/<str:game_id>/', views.input_view, name='input_view'),
    path('<str:game_id>/<str:player_id>/', views.modify_player, name='modify_player'),
    path('<str:game_id>/<str:player_id>/input/', views.change_player_name, name='change_player_name'),
    path('<str:game_id>/<str:player_id>/remove/', views.empty_player_name, name='empty_player_name'),
    # path('players/', views.players, name='players'),
    path('<str:game_id>/', views.players, name='players'),

    # path('reservations/', views.Table, name='reservations'),
]