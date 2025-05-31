# users/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def sentry_test_error(request):
    # Gooi een opzettelijke fout
    1 / 0  # ZeroDivisionError
    return Response({"detail": "Dit zal nooit geretourneerd worden"})
