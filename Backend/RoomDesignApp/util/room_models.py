import uuid
from Backend.RoomDesignApp.models import Room, RoomModel
from Backend.RoomDesignApp.util.auth import handle_admin
from Backend.RoomDesignApp.util.model import (
    handle_get_model_by_id,
    model_to_json_serializer,
)
from Backend.RoomDesignApp.util.room import handle_get_room_by_id


def room_model_to_json_serializer(room_model: RoomModel):
    """
    Converts a room_model object to a JSON serializable dictionary.
    """

    return {
        "model": model_to_json_serializer(room_model.model),
        "id": room_model.id,
        "size": room_model.size,
        "rotations": room_model.rotations,
        "axis": room_model.axis,
    }


def handle_get_all_room_models_for_room(room_id: str) -> list[dict]:
    """
    Returns all RoomModel objects belonging to rooms owned by the given user,
    in JSON serializable format.

    Args:
        room_id: ID of the user whose room models are to be retrieved

    Returns:
        List of serialized RoomModel dictionaries
    """
    return list(RoomModel.objects.filter(room_id=room_id).order_by("-id"))


def handle_get_room_model_by_id(
    user_id: str, room_model_id: uuid.UUID
) -> tuple[RoomModel | None, bool, str]:
    """
    Returns a RoomModel instance by its ID, ensuring the user owns the related room.

    Args:
        user_id: ID of the user who owns the room
        room_model_id: ID of the RoomModel to retrieve

    Returns:
        Tuple of (RoomModel instance or None, success_bool, message)
    """

    is_admin, message = handle_admin(user_id)

    try:
        room_model = RoomModel.objects.get(id=room_model_id)
        if str(room_model.room.owner.id) != str(user_id) and not is_admin:
            return (None, False, "You do not have permission to access this model")
        return (room_model, True, "Room model found")
    except RoomModel.DoesNotExist:
        return (None, False, "Room model not found with the given ID")


def handle_update_room_model(
    user_id: str, room_model_id: str, room_model_data: dict
) -> tuple[bool, str]:
    """
    Updates an existing room model in the database.

    Args:
        user_id: ID of the user who owns the room model
        room_model_id: ID of the RoomModel to update
        room_model_data: A dictionary containing the updated fields (e.g., size, axis, rotations)

    Returns:
        Tuple of (success_bool, message)
    """

    room_model, success, message = handle_get_room_model_by_id(user_id, room_model_id)

    if not success:
        return False, message

    allowed_fields = {"size", "axis", "rotations"}

    for attr, value in room_model_data.items():
        if attr in allowed_fields:
            setattr(room_model, attr, value)

    room_model.save()

    return True, f"Room model '{room_model.id}' has been updated successfully"


def handle_add_model_to_room(
    user_id: str, room_id: str, model_id: str
) -> tuple[bool, str]:
    """
    Adds a model to a room.

    Args:
        user_id: ID of the user who owns the room
        room_id: ID of the room
        model_id: ID of the model to add

    Returns:
        Tuple of (success_bool, message)
    """
    room, success_room, message_room = handle_get_room_by_id(user_id, room_id)
    model, success_model, message_model = handle_get_model_by_id(model_id)

    if not success_room:
        return False, message_room

    if not success_model:
        return False, message_model

    try:
        RoomModel.objects.create(
            room=room,
            model=model,
            size=model.size,
            rotations=model.rotations,
            axis=model.axis,
        )

        return True, f"Model '{model.name}' has been added to room '{room.name}'"

    except Exception as e:
        return False, f"Error adding model to room: {str(e)}"


def remove_room_model(user_id: str, room_model_id: str) -> tuple[bool, str]:
    """
    Removes a room model from a room.

    Args:
        user_id: ID of the user requesting the deletion (validated through ownership)
        room_model_id: ID of the RoomModel to remove

    Returns:
        Tuple of (success_bool, message)
    """
    try:
        room_model = RoomModel.objects.get(id=room_model_id)

        is_admin, message = handle_admin(user_id)

        if str(room_model.room.owner.id) != str(user_id) and not is_admin:
            return False, "You do not have permission to delete this model."

        room_model.delete()
        return True, "Room model removed successfully."

    except RoomModel.DoesNotExist:
        return False, "Room model not found."

    except Exception as e:

        return False, f"Error removing room model: {str(e)}"
