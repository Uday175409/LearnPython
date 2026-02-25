# ============================================================
# api/urls.py — API URL Routing
# ============================================================
# These match the exact endpoints the React frontend calls.
# ============================================================

from django.urls import path
from . import views

urlpatterns = [
    # ── Auth ─────────────────────────────────────────────────
    path("auth/register", views.register),
    path("auth/login", views.login),
    path("auth/me", views.me),

    # ── Courses & Lessons ────────────────────────────────────
    path("courses", views.list_courses),
    path("courses/<int:course_id>/lessons", views.list_lessons),
    path("lessons/<int:lesson_id>", views.get_lesson),

    # ── Exercises ────────────────────────────────────────────
    path("exercises/<int:exercise_id>", views.get_exercise),
    path("exercises/<int:exercise_id>/solution", views.get_solution),
    path("exercises/<int:exercise_id>/submit", views.submit_exercise),

    # ── Code Execution ───────────────────────────────────────
    path("run", views.run_code),

    # ── Progress ─────────────────────────────────────────────
    path("progress", views.get_progress),
    path("lessons/<int:lesson_id>/complete", views.mark_lesson_complete),
]
