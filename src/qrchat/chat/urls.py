from django.urls import path

from .views import chat_lobby_view, chat_room_view


app_name = 'chat'

urlpatterns = [
    path('lobby/<str:room_id>/', chat_lobby_view.ChatLobby.as_view(), name='chat_lobby'),
    path('room/<str:room_id>/', chat_room_view.ChatRoom.as_view(), name='chat_room'),
]