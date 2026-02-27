# ============================================================
# learnpython/urls.py — Project URL Configuration
# ============================================================

from django.urls import path, include
from api.views import root, health

urlpatterns = [
    # All API routes are under /api/
    path("api/", include("api.urls")),

    # Health checks at root
    path("", root),
    path("health", health),
]
