import uuid
from Backend.RoomDesignApp.models import Account, Room, RoomModel
from Backend.RoomDesignApp.util.auth import handle_admin
from Backend.RoomDesignApp.util.room_models import (
    handle_get_all_room_models_for_room,
    room_model_to_json_serializer,
)


def room_to_json_serializer(room: Room):
    """
    Converts a room object to a JSON serializable dictionary.
    """
    return {
        "id": room.id,
        "name": room.name,
        "description": room.description,
        "room_file": room.room_file.url if room.room_file else None,
        "room_models": [
            room_model_to_json_serializer(room_model)
            for room_model in handle_get_all_room_models_for_room(room.id)
        ],
    }


def handle_get_rooms_list(user_id) -> list[Room]:
    """
    Returns a list of all rooms in JSON serializable format.
    This function retrieves all rooms from the database and orders them by creation date.

    Args:
        user_id: ID of the user whose rooms are to be retrieved

    Returns:
        List of Room instances ordered by creation date in descending order.
    """

    return list(Room.objects.filter(owner_id=user_id).order_by("-created_at"))


def handle_get_room_by_id(
    user_id: str, room_id: uuid.UUID
) -> tuple[Room | None, bool, str]:
    """
    Returns a room instance by its ID.

    Args:
        room_id: ID of the room to retrieve
        user_id: ID of the user who owns the room

    Returns:
        Tuple of (Room instance, success_bool, message)
    """
    is_admin, message = handle_admin(user_id)

    try:
        if is_admin:
            return (Room.objects.get(id=room_id), True, "Room found")
        return (Room.objects.get(id=room_id, owner_id=user_id), True, "Room found")
    except Room.DoesNotExist:
        return (None, False, "Room not found with the given ID")


def handle_add_room(roomData: dict) -> tuple[bool, str]:
    """
    Adds a new room to the database.

    Args:
        data: A dictionary containing the room data.

    Returns:
        Tuple of (success_bool, message)
    """

    if (
        not roomData.get("name")
        or not roomData.get("owner_id")
        or not roomData.get("description")
        or not roomData.get("room_file")
    ):
        return (False, "Name, description, and room file are required")

    owner = Account.objects.get(user_id=roomData.get("owner_id"))

    room = Room.objects.create(
        name=roomData["name"],
        description=roomData.get("description", ""),
        room_file=roomData["room_file"],
        owner=owner,
    )

    return (True, f"Room '{room.name}' has been added successfully")


def handle_update_room(user_id: str, room_id: str, roomData: dict) -> tuple[bool, str]:
    """
    Updates an existing room in the database.

    Args:
        room_id: ID of the room to update
        user_id: ID of the user who owns the room
        roomData: A dictionary containing the updated room data.

    Returns:
        Tuple of (success_bool, message)
    """

    room, success, message = handle_get_room_by_id(user_id, room_id)

    if not success:
        return (False, message)

    for attr, value in roomData.items():
        if hasattr(room, attr):
            setattr(room, attr, value)

    room.save()
    return (True, f"Room '{room.name}' has been updated successfully")


def handle_delete_room(user_id: str, room_id: str) -> tuple[bool, str]:
    """
    Deletes a room from the database.

    Args:
        room_id: ID of the room to delete
        user_id: ID of the user who owns the room

    Returns:
        Tuple of (success_bool, message)
    """

    room, success, message = handle_get_room_by_id(user_id, room_id)

    if not success:
        return (False, message)

    room.delete()
    return (True, f"Room '{room.name}' has been deleted successfully")
