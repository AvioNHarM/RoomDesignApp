from difflib import SequenceMatcher
import uuid
from Backend.RoomDesignApp.models import Model
from django.db.models import QuerySet


def model_to_json_serializer(model: Model):
    """
    Converts a model object to a JSON serializable dictionary.

    Args:
        model: Model instance to serialize
    Returns:
        Dictionary containing model attributes in a JSON serializable format.
    """

    return {
        "id": str(model.id),
        "name": model.name,
        "description": model.description,
        "tags": model.tags,
        "listed": model.listed,
        "img": model.img.url if model.img else None,
        "model_file": model.model_file.url if model.model_file else None,
        "axis": model.axis,
        "rotations": model.rotations,
        "size": model.size,
    }


def handle_get_models_list() -> list[Model]:
    """
    Returns a list of all models in JSON serializable format.
    This function retrieves all models from the database and orders them by creation date.

    Returns:
        List of Model instances ordered by creation date in descending order.
    """

    return list(Model.objects.all().order_by("-created_at"))


def handle_get_model_by_id(model_id: uuid.UUID) -> tuple[Model | None, bool, str]:
    """
    Returns a model instance by its ID.

    Args:
        model_id: UUID of the model to retrieve
    Returns:
        Tuple of (Model instance, success_bool, message)
    """
    try:
        return (Model.objects.get(id=model_id), True, "Model found")

    except Model.DoesNotExist:

        return (None, False, "Model not found with the given ID")


def handle_add_model(
    modelData: dict,
) -> tuple[bool, str]:
    """
    Adds a new model to the database.

    Args:
        modelData: Dictionary containing model data with keys:

            - name: Name of the model
            - model_file: File path of the model
            - description: Description of the model
            - axis: Axis data (optional)
            - rotations: Rotation data (optional)
            - size: Size of the model (optional, default is 1)
            - img: Image file path (optional)
            - tags: List of tags (optional)
    Returns:
        Tuple of (success_bool, message)
    """

    if (
        not modelData.get("name")
        or not modelData.get("model_file")
        or not modelData.get("description")
    ):
        return (False, "Model name, file, and description are required")

    model = Model.objects.create(
        name=modelData["name"],
        description=modelData["description"],
        model_file=modelData["model_file"],
        axis=modelData["axis"] if modelData.get("axis") else [],
        rotations=modelData["rotations"] if modelData.get("rotations") else [],
        size=modelData["size"] if modelData.get("size") else 1,
        img=modelData.get("img") if modelData.get("img") else None,
        tags=modelData["tags"] if modelData.get("tags") else [],
    )
    return (True, f"Model '{model.name}' added successfully with ID {model.id}")


def handle_delete_model(model_id: uuid.UUID) -> tuple[bool, str]:
    """
    Deletes a model from the database.

    Args:
        model_id: ID of the model to delete

    Returns:
        Tuple of (success_bool, message)
    """

    model, success, message = handle_get_model_by_id(model_id)

    if not success:
        return (False, message)

    model.delete()
    return (True, f"Model '{model.name}' deleted successfully")


def handle_update_model(model_id: uuid.UUID, update_data: dict) -> tuple[bool, str]:
    """
    Updates an existing model with the provided data.

    Args:
        model_id: ID of the model to update
        update_data: Dictionary containing fields to update

    Returns:
        Tuple of (success_bool, message)
    """

    model, success, message = handle_get_model_by_id(model_id)

    if not success:
        return (False, message)

    for attr, value in update_data.items():
        if hasattr(model, attr):
            setattr(model, attr, value)

    model.save()
    return (True, f"Model '{model.name}' updated successfully")


def handle_unlist_model(model_id: uuid.UUID) -> tuple[bool, str]:
    """
    Unlists a model by setting its 'listed' attribute to False.

    Args:
        model_id: ID of the model to unlist

    Returns:
        Tuple of (success_bool, message)
    """

    model, success, message = handle_get_model_by_id(model_id)

    if not success:
        return (False, message)

    model.listed = False
    model.save()
    return (True, f"Model '{model.name}' has been unlisted successfully")


def handle_search_product_by_token(
    token: str, min_similarity: float = 0.6
) -> tuple[QuerySet | None, bool, str]:
    """
    Search for products by token with improved similarity matching.

    Args:
        token: Search term
        min_similarity: Minimum similarity score to consider a match (0.0 to 1.0)

    Returns:
        Tuple of (QuerySet, success_bool, message)
    """

    def calculate_similarity_score(product_name: str, search_token: str) -> float:
        """
        Calculate similarity score between product name and search token.
        Returns a score between 0 and 1, where 1 is a perfect match.
        """
        product_lower = product_name.lower().strip()
        print(f"Product Lower: {product_lower}")
        token_lower = search_token.lower().strip()

        if token_lower == product_lower:
            return 1.0

        if token_lower in product_lower:
            return 0.8 + (len(token_lower) / len(product_lower)) * 0.2

        similarity = SequenceMatcher(None, product_lower, token_lower).ratio()

        return similarity if similarity >= 0.6 else 0.0

    token = token.strip() if token else ""

    if len(token) < 2:
        return (
            Model.objects.none(),
            False,
            "Search term must be at least 2 characters long.",
        )

    candidates = Model.objects.filter(name__icontains=token)

    if not candidates.exists():
        candidates = Model.objects.all()[:1000]

    matched_models = []
    for model in candidates:
        similarity_score = calculate_similarity_score(model.name, token)
        if similarity_score >= min_similarity:
            matched_models.append((model, similarity_score))

    if not matched_models:
        return (Model.objects.none(), False, "No models matched the search term.")

    matched_models.sort(key=lambda x: x[1], reverse=True)
    matched_model_ids = [model.id for model, _ in matched_models]

    final_queryset = Model.objects.filter(id__in=matched_model_ids)

    preserved_order = {id: index for index, id in enumerate(matched_model_ids)}
    final_queryset = sorted(final_queryset, key=lambda x: preserved_order[x.id])

    return (
        final_queryset,
        True,
        f"Found {len(matched_models)} models matching the search term.",
    )
