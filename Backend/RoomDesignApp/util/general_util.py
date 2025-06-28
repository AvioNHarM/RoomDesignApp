from django.http import JsonResponse


def errorResponse(message: str, status: int = 400) -> JsonResponse:
    return JsonResponse({"error": message}, status=status)
