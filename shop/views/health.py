from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response


@extend_schema(
    request=None, responses={200: OpenApiResponse(description="OK", response=None)}
)
@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok"})
