from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_room/", views.create_room, name="create_room"),
    path("room/<str:room_name>/", views.room, name="room"),
    path("end_room/<str:room_id>/", views.end_room, name="end_room"),
    path("upload_recording/", views.upload_recording, name="upload_recording"),
]
