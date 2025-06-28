from django.urls import path
from . import views

urlpatterns = [
    # Room URLs
    path("rooms/", views.get_rooms_view, name="get_rooms"),
    path("room/get/", views.get_room_view, name="get_room"),
    path(
        "room_model/get/", views.get_room_model_by_id_view, name="get_room_model_by_id"
    ),  # <-- added
    path("rooms/add/", views.add_room_view, name="add_room"),
    path(
        "rooms/add_model/", views.add_room_model_to_room_view, name="add_model_to_room"
    ),
    path("rooms/update/", views.update_room_view, name="update_room"),
    path("rooms/delete/", views.delete_room_view, name="delete_room"),
    # RoomModel URLs
    path("room_models/update/", views.update_room_model_view, name="update_room_model"),
    path("room_models/delete/", views.delete_room_model_view, name="delete_room_model"),
    # Model URLs
    path("models/", views.get_models_view, name="get_models"),
    path("model/get/", views.get_model_view, name="get_model"),
    path("models/add/", views.add_model_view, name="add_model"),
    path("models/update/", views.update_model_view, name="update_model"),
    path("models/delete/", views.delete_model_view, name="delete_model"),
    path("models/search/", views.search_model_view, name="search_model"),
    path("models/unlist/", views.unlist_model_view, name="unlist_model"),
    # Auth URLs
    path("auth/login/", views.login, name="login"),
    path("auth/signup/", views.signup, name="signup"),
    path("auth/is_admin/", views.is_admin, name="is_admin"),
]
