import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import Backend.RoomDesignApp.util.auth as auth_utils
import RoomDesignApp.util.model as model_utils
import Backend.RoomDesignApp.util.room as room_utils
import Backend.RoomDesignApp.util.room_models as room_model_utils
from Backend.RoomDesignApp.util.general_util import errorResponse


# Create your views here.


# RoomModelViews
@csrf_exempt
def add_room_model_to_room_view(request):
    """
    Adds a model to a room.
    This view handles adding an existing model to a specific room by processing
    form data submitted via a POST request.
    Expects POST form data:
        - userid: <str> (required, ID of the user who owns the room)
        - roomid: <str> (required, ID of the room)
        - modelid: <str> (required, ID of the model to add)
    Returns:
        JsonResponse: A JSON response indicating success or failure of adding the model to the room.
    """
    if request.method != "POST":
        return errorResponse("Only POST method allowed", status=405)

    try:
        user_id = request.POST.get("userid")
        room_id = request.POST.get("roomid")
        model_id = request.POST.get("modelid")
    except Exception as e:
        return errorResponse(f"Server error: {str(e)}", status=500)

    if not user_id or not room_id or not model_id:
        return errorResponse("Missing required fields", status=400)

    success, message = room_model_utils.handle_add_model_to_room(
        user_id, room_id, model_id
    )

    if success:
        return JsonResponse({"message": message}, status=201)
    return errorResponse(message, status=400)


@csrf_exempt
def update_room_model_view(request):
    """
    Updates a room model.
    This view handles updating properties of an existing room model by processing
    form data submitted via a POST request.
    Expects POST form data:
        - userid: <str> (required, ID of the user who owns the room)
        - id: <str> (required, ID of the RoomModel to update)
        - room_model_data: <JSON> (required, the updated room model data)
    Returns:
        JsonResponse: A JSON response indicating success or failure of the room model update.
    """
    if request.method != "POST":
        return errorResponse("Only POST method allowed", status=405)

    try:
        user_id = request.POST.get("userid")
        room_model_id = request.POST.get("id")
        room_model_data = request.POST.get("room_model_data", "{}")
    except Exception as e:
        return errorResponse(f"Server error: {str(e)}", status=500)

    if not user_id or not room_model_id:
        return errorResponse("Missing required fields", status=400)

    success, message = room_model_utils.handle_update_room_model(
        user_id, room_model_id, room_model_data
    )

    if success:
        return JsonResponse({"message": message}, status=200)
    return errorResponse(message, status=400)


@csrf_exempt
def delete_room_model_view(request):
    """
    Deletes a room model from a room.
    This view handles the deletion of a room model by its ID, which is expected to be provided
    in the POST request body.
    Expects a POST request with the following form data:
        - id: <str> (required, the ID of the room model to delete)
        - userid: <str> (required, the ID of the user making the request)
    Returns:
        JsonResponse: A JSON response indicating success or failure of the room model deletion.
    """
    if request.method != "POST":
        return errorResponse("Only POST method allowed", status=405)

    try:
        room_model_id = request.POST.get("id")
        user_id = request.POST.get("userid")

    except Exception as e:
        return errorResponse(f"Server error: {str(e)}", status=500)

    if not room_model_id or not user_id:
        return errorResponse("Missing required fields", status=400)

    success, message = room_model_utils.remove_room_model(user_id, room_model_id)

    if success:
        return JsonResponse({"message": message}, status=200)
    return errorResponse(message, status=400)


def get_room_model_by_id_view(request):
    """
    Retrieves a specific room model by its ID.
    This view handles the retrieval of a single room model owned by a user via a GET request.
    Expects GET parameters:
        - userid: <str> (required, ID of the user who owns the room)
        - id: <str> (required, ID of the room model to retrieve)
    Returns:
        JsonResponse: A JSON response containing the room model data or an error message.
    """
    if request.method != "GET":
        return errorResponse("Only GET method allowed", status=405)

    try:
        user_id = request.GET.get("userid")
        room_model_id = request.GET.get("id")
    except Exception as e:
        return errorResponse(f"Server error: {str(e)}", status=500)

    if not user_id or not room_model_id:
        return errorResponse("Missing required fields", status=400)

    room_model, success, message = room_model_utils.handle_get_room_model_by_id(
        user_id, room_model_id
    )

    if not success:
        return errorResponse(message, status=400)

    serialized_room_model = room_model_utils.room_model_to_json_serializer(room_model)
    return JsonResponse({"room_model": serialized_room_model}, status=200)


# RoomViews
@csrf_exempt
def get_rooms_view(request):
    """
    Retrieves all rooms for a specific user.
    This view handles the retrieval of all rooms owned by a user via a GET request.
    Expects GET parameters:
        - userid: <str> (required, ID of the user whose rooms are to be retrieved)
    Returns:
        JsonResponse: A JSON response containing the list of rooms or an error message.
    """
    if request.method != "GET":
        return errorResponse("Only GET method allowed", status=405)

    try:
        user_id = request.GET.get("userid")
    except Exception as e:
        return errorResponse(f"Server error: {str(e)}", status=500)

    if not user_id:
        return errorResponse("Missing required field: userid", status=400)

    rooms = room_utils.handle_get_rooms_list(user_id)
    serialized_rooms = [room_utils.room_to_json_serializer(room) for room in rooms]

    return JsonResponse({"rooms": serialized_rooms}, status=200)


@csrf_exempt
def get_room_view(request):
    """
    Retrieves a specific room by its ID.
    This view handles the retrieval of a single room owned by a user via a GET request.
    Expects GET parameters:
        - userid: <str> (required, ID of the user who owns the room)
        - id: <str> (required, ID of the room to retrieve)
    Returns:
        JsonResponse: A JSON response containing the room data or an error message.
    """
    if request.method != "GET":
        return errorResponse("Only GET method allowed", status=405)

    try:
        user_id = request.GET.get("userid")
        room_id = request.GET.get("id")
    except Exception as e:
        return errorResponse(f"Server error: {str(e)}", status=500)

    if not user_id or not room_id:
        return errorResponse("Missing required fields", status=400)

    room, success, message = room_utils.handle_get_room_by_id(user_id, room_id)

    if not success:
        return errorResponse(message, status=400)

    serialized_room = room_utils.room_to_json_serializer(room)
    return JsonResponse({"room": serialized_room}, status=200)


@csrf_exempt
def delete_room_view(request):
    """
    Deletes a room from the database.
    This view handles the deletion of a room by its ID, which is expected to be provided
    in the POST request body.
    Expects a POST request with the following form data:
        - id: <str> (required, the ID of the room to delete)
        - userid: <str> (required, the ID of the user making the request)
    Returns:
        JsonResponse: A JSON response indicating success or failure of the room deletion.
    """
    if request.method != "POST":
        return errorResponse("Only POST method allowed", status=405)

    try:
        room_id = request.POST.get("id")
        user_id = request.POST.get("userid")
    except Exception as e:
        return errorResponse(f"Server error: {str(e)}", status=500)

    if not room_id or not user_id:
        return errorResponse("Missing required fields", status=400)

    success, message = room_utils.handle_delete_room(user_id, room_id)

    if success:
        return JsonResponse({"message": message}, status=200)
    return errorResponse(message, status=400)


@csrf_exempt
def update_room_view(request):
    """
    Updates an existing room with the provided data.
    This view handles the update of a room by processing form data submitted via a POST request.
    Expects POST form data:
        - id: <str> (required, the ID of the room to update)
        - room_data: <JSON> (required, the updated room data)
        - userid: <str> (required, the ID of the user making the request)
    Returns:
        JsonResponse: A JSON response indicating success or failure of the room update.
    """
    if request.method != "POST":
        return errorResponse("Only POST method allowed", status=405)

    try:
        room_id = request.POST.get("id")
        user_id = request.POST.get("userid")
        room_data = request.POST.get("room_data", "{}")
    except Exception as e:
        return errorResponse(f"Server error: {str(e)}", status=500)

    if not room_id or not user_id:
        return errorResponse("Missing required fields", status=400)

    success, message = room_utils.handle_update_room(user_id, room_id, room_data)

    if success:
        return JsonResponse({"message": message}, status=200)
    return errorResponse(message, status=400)


@csrf_exempt
def add_room_view(request):
    """
    Adds a new room to the database.
    This view handles the addition of a new room by processing multipart form data
    submitted via a POST request.
    Expects multipart form data:
        - name: <str> (required)
        - description: <str> (required)
        - room_file: <file> (required)
        - userid: <str> (required, ID of the user creating the room)
    Returns:
        JsonResponse: A JSON response indicating success or failure of the room addition.
    """
    if request.method != "POST":
        return errorResponse("Only POST method allowed", status=405)

    if not request.content_type.startswith("multipart/form-data"):
        return errorResponse("Expected multipart form data", status=400)

    try:
        user_id = request.POST.get("userid")
        name = request.POST.get("name")
        description = request.POST.get("description")
        room_file = request.FILES.get("room_file")
    except Exception as e:
        return errorResponse(f"Server error: {str(e)}", status=500)

    if not user_id or not name or not description or not room_file:
        return errorResponse("Missing required fields", status=400)

    data = {
        "name": name,
        "description": description,
        "room_file": room_file,
        "owner_id": user_id,
    }

    success, message = room_utils.handle_add_room(data)

    if success:
        return JsonResponse({"message": message}, status=201)
    return errorResponse(message, status=400)


# ModelsViews
def get_models_view(request):
    """
    Retrieves a list of all models in JSON serializable format.
    This function fetches all models from the database and serializes them into a JSON response.

    Args:
        - No parameters are required in the request.

    Returns:
        - JsonResponse: A JSON response containing a list of serialized model objects.

    """

    models = model_utils.handle_get_models_list()

    serialized_models = [
        model_utils.model_to_json_serializer(model) for model in models
    ]

    return JsonResponse(serialized_models, safe=False, status=200)


def get_model_view(request):

    try:
        model_id = request.GET.get("id")
    except (TypeError, ValueError):
        return errorResponse("Invalid model ID", status=400)

    if not model_id:
        return errorResponse("Model ID is required", status=400)

    model, success, message = model_utils.handle_get_model_by_id(model_id)

    if not success:
        return errorResponse(message, status=404)

    return JsonResponse(
        model_utils.model_to_json_serializer(model), safe=False, status=200
    )


@csrf_exempt
def add_model_view(request):
    """
    Adds a new model to the database.
    This view handles the addition of a new model by processing form data and files
    submitted via a POST request. It requires admin privileges to access.

    Expects multipart form data:
        - name: <str>
        - description: <str>
        - tags: <str> (comma-separated)
        - listed: <bool> (default: false)
        - img: <file> (optional)
        - model_file: <file> (required)
        - axis: <str> (optional)
        - rotations: <str> (optional)

    Returns:
        JsonResponse: A JSON response indicating success or failure of the model addition.
    """

    if request.method != "POST":
        return errorResponse("Only POST method allowed", status=405)

    if not request.content_type.startswith("multipart/form-data"):
        return errorResponse("Expected multipart form data", status=400)

    product_data = request.POST

    image_file = request.FILES.get("img")

    userid = product_data.get("userid")

    is_admin, message = auth_utils.handle_admin(userid)

    if not is_admin:
        return errorResponse("Unauthorized: Admin access required", status=403)

    data = {
        "name": product_data.get("name"),
        "description": product_data.get("description"),
        "tags": product_data.get("tags", "").split(","),
        "listed": product_data.get("listed", "false").lower() == "true",
        "img": image_file,
        "model_file": request.FILES.get("model_file"),
        "axis": product_data.get("axis", ""),
        "rotations": product_data.get("rotations", ""),
        "size": product_data.get("size", ""),
    }

    success, message = model_utils.handle_add_model(data)
    if success:
        return JsonResponse({"message": message}, status=201)

    return errorResponse(message, status=400)


@csrf_exempt
def delete_model_view(request):
    """
    Deletes a model from the database.
    This view handles the deletion of a model by its ID, which is expected to be provided
    in the POST request body. It requires admin privileges to access.

    Expects a POST request with the following form data:
        - id: <UUID> (required, the ID of the model to delete)
        - userid: <str> (required, the ID of the user making the request)

    Returns:
        JsonResponse: A JSON response indicating success or failure of the model deletion.
    """

    if request.method != "POST":
        return errorResponse("Only POST method allowed", status=405)

    try:
        model_id = uuid.UUID(request.POST.get("id"))
        user_id = request.POST.get("userid")

    except (TypeError, ValueError):
        return errorResponse("Invalid model ID", status=400)

    is_admin, message = auth_utils.handle_admin(user_id)

    if not is_admin:
        return errorResponse("Unauthorized: Admin access required", status=403)

    success, message = model_utils.handle_delete_model(model_id)

    if not success:
        return errorResponse(message, status=400)

    return JsonResponse({"message": message}, status=200)


@csrf_exempt
def update_model_view(request):
    """
    Updates an existing model with the provided data.
    This view handles the update of a model by processing form data and files
    submitted via a POST request. It requires admin privileges to access.

    Expects multipart form data:
        - id: <UUID> (required, the ID of the model to update)
        - model_data: <JSON> (required, the updated model data)
        - userid: <str> (required, the ID of the user making the request)

    Returns:
        JsonResponse: A JSON response indicating success or failure of the model update.

    """

    if request.method != "POST":
        return errorResponse("Only POST method allowed", status=405)

    try:
        model_id = uuid.UUID(request.POST.get("id"))
        user_id = request.POST.get("userid")
        model_data = request.POST.get("model_data", "{}")

    except (TypeError, ValueError):
        return errorResponse("Invalid model ID or data", status=400)

    is_admin, message = auth_utils.handle_admin(user_id)

    if not is_admin:
        return errorResponse("Unauthorized: Admin access required", status=403)

    success, message = model_utils.handle_update_model(model_id, model_data)

    if not success:
        return errorResponse(message, status=400)

    return JsonResponse({"message": message}, status=200)


def search_model_view(request):
    """
    Searches for models based on a search token.
    This view retrieves models that match the provided search token.

    Expects a GET request with the following query parameter:
        - search_token: <str> (required, the token to search for in model names
            or descriptions)

    Returns:
        JsonResponse: A JSON response containing a list of models that match the search token.
    """

    try:
        search_token = request.GET.get("search_token", None)

    except (TypeError, ValueError):
        return errorResponse("Invalid search token", status=400)

    models, success, message = model_utils.handle_search_product_by_token(search_token)

    if not success:
        return errorResponse(message, status=404)

    return JsonResponse(
        [model_utils.model_to_json_serializer(model) for model in models],
        safe=False,
        status=200,
    )


@csrf_exempt
def unlist_model_view(request):
    """
    Unlists a model by its ID.

    This view handles the unlisting of a model by processing a POST request
    containing the model ID. It requires admin privileges to access.
    Expects a POST request with the following form data:
        - id: <UUID> (required, the ID of the model to unlist)
        - userid: <str> (required, the ID of the user making the request)

    Returns:
        JsonResponse: A JSON response indicating success or failure of the unlisting operation.
    """

    if request.method != "POST":
        return errorResponse("Only POST method allowed", status=405)

    try:
        model_id = uuid.UUID(request.POST.get("id"))
        user_id = request.POST.get("userid")
    except (TypeError, ValueError):
        return errorResponse("Invalid model ID", status=400)

    is_admin, message = auth_utils.handle_admin(user_id)

    if not is_admin:
        return errorResponse("Unauthorized: Admin access required", status=403)

    success, message = model_utils.handle_unlist_model(model_id)
    if not success:
        return errorResponse(message, status=400)

    return JsonResponse({"message": message}, status=200)


# AuthViews
@csrf_exempt
def login(request):
    """
    Handles user login by checking the provided username and password.
    Expects a POST request with the following form data:
        - username: <str> (required)
        - email: <str> (required)
        - password: <str> (required)

    Returns:
        JsonResponse: A JSON response indicating success or failure of the login attempt.
    """
    if request.method != "POST":
        return errorResponse("Only POST method allowed", status=405)

    try:
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

    except (TypeError, ValueError):
        return errorResponse("Invalid username or password", status=400)

    account, success, message = auth_utils.handle_login(username, email, password)

    if not success:
        return errorResponse(message, status=400)

    return JsonResponse({"message": message, "user_id": str(account.id)}, status=200)


@csrf_exempt
def signup(request):
    """
    Handles user signup by creating a new account.
    Expects a POST request with the following form data:
        - username: <str> (required)
        - email: <str> (required)
        - password: <str> (required)

    Returns:
        JsonResponse: A JSON response indicating success or failure of the signup attempt.
    """
    if request.method != "POST":
        return errorResponse("Only POST method allowed", status=405)

    try:
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

    except (TypeError, ValueError):
        return errorResponse("Invalid username, email, or password", status=400)

    account, success, message = auth_utils.handle_register(email, username, password)

    if not success:
        return errorResponse(message, status=400)

    return JsonResponse({"message": message, "user_id": str(account.id)}, status=201)


def is_admin(request):
    """
    Checks if the user is an admin.
    Expects a POST request with the following form data:
        - userid: <str> (required)

    Returns:
        JsonResponse: A JSON response indicating whether the user is an admin.
    """
    if request.method != "POST":
        return errorResponse("Only POST method allowed", status=405)

    user_id = request.POST.get("userid")

    is_admin, message = auth_utils.handle_admin(user_id)

    if not is_admin:
        return errorResponse(message, status=403)

    return JsonResponse({"message": message}, status=200)
