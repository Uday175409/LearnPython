# ============================================================
# api/views.py — All API Views (No Authentication)
# ============================================================
# All endpoints are public — no login required.
#
#   GET  /api/courses
#   GET  /api/courses/:id/lessons
#   GET  /api/lessons/:id
#   GET  /api/exercises/:id
#   GET  /api/exercises/:id/solution
#   POST /api/run
#   POST /api/exercises/:id/submit
#   GET  /           (health check)
#   GET  /health     (health check)
# ============================================================

import asyncio
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Course, Lesson, Exercise
from .serializers import (
    CourseOutSerializer,
    LessonDetailSerializer,
    ExerciseOutSerializer,
)
from sandbox import execute_code, run_exercise_tests
from error_explainer import explain_error


# ── Helpers ──────────────────────────────────────────────────

def _run_async(coro):
    """Run an async coroutine from sync Django view code."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                return pool.submit(asyncio.run, coro).result()
        return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)


# ════════════════════════════════════════════════════════════
# COURSE & LESSON VIEWS
# ════════════════════════════════════════════════════════════

@api_view(["GET"])
@permission_classes([AllowAny])
def list_courses(request):
    """Return all courses, ordered by sequence."""
    courses = Course.objects.all()
    serializer = CourseOutSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def list_lessons(request, course_id):
    """Return all lessons in a course. All lessons are unlocked."""
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return Response(
            {"detail": "Course not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    lessons = course.lessons.all().order_by("order")

    result = []
    for lesson in lessons:
        result.append({
            "id": lesson.id,
            "course_id": lesson.course_id,
            "title": lesson.title,
            "subtitle": lesson.subtitle or "",
            "order": lesson.order,
            "is_completed": False,
            "is_locked": False,
        })

    return Response(result)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_lesson(request, lesson_id):
    """Return the full content of a lesson plus its exercises."""
    try:
        lesson = Lesson.objects.prefetch_related("exercises").get(pk=lesson_id)
    except Lesson.DoesNotExist:
        return Response(
            {"detail": "Lesson not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = LessonDetailSerializer(lesson)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_exercise(request, exercise_id):
    """Return exercise details (without the solution)."""
    try:
        exercise = Exercise.objects.get(pk=exercise_id)
    except Exercise.DoesNotExist:
        return Response(
            {"detail": "Exercise not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = ExerciseOutSerializer(exercise)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_solution(request, exercise_id):
    """Reveal the full solution and explanation for an exercise."""
    try:
        exercise = Exercise.objects.get(pk=exercise_id)
    except Exercise.DoesNotExist:
        return Response(
            {"detail": "Exercise not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response({
        "solution": exercise.solution or "",
        "explanation": exercise.explanation or "",
    })


# ════════════════════════════════════════════════════════════
# CODE EXECUTION VIEWS
# ════════════════════════════════════════════════════════════

@api_view(["POST"])
@permission_classes([AllowAny])
def run_code(request):
    """Execute Python code and return the output (playground)."""
    code = request.data.get("code", "")
    if not code:
        return Response(
            {"detail": "No code provided."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    result = _run_async(execute_code(code))

    friendly_error = ""
    if result["error"]:
        friendly_error = explain_error(result["error"])

    return Response({
        "output": result["output"],
        "error": result["error"],
        "friendly_error": friendly_error,
        "execution_time_ms": result["execution_time_ms"],
    })


@api_view(["POST"])
@permission_classes([AllowAny])
def submit_exercise(request, exercise_id):
    """Submit code for an exercise, run tests, and grade it."""
    try:
        exercise = Exercise.objects.get(pk=exercise_id)
    except Exercise.DoesNotExist:
        return Response(
            {"detail": "Exercise not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    code = request.data.get("code", "")
    if not code:
        return Response(
            {"detail": "No code provided."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Run the code against test cases
    result = _run_async(run_exercise_tests(
        code=code,
        tests=exercise.tests or [],
    ))

    friendly_error = ""
    if result["error"]:
        friendly_error = explain_error(result["error"])

    # Build a user-friendly message
    if result["is_correct"]:
        message = (
            "🎉 **Great job!** All tests passed! "
            "You got it right. Keep going!"
        )
    else:
        failed = next(
            (t for t in result["test_results"] if not t["passed"]),
            None,
        )
        if failed and not result["error"]:
            message = (
                f"❌ **Not quite right.** "
                f"Test {failed['test_number']} expected the output to be:\n\n"
                f"```\n{failed['expected']}\n```\n\n"
                f"But your code produced:\n\n"
                f"```\n{failed['actual']}\n```\n\n"
                f"Look at the difference carefully and try again!"
            )
        elif result["error"]:
            message = "❌ **Your code has an error.** See the explanation below."
        else:
            message = "❌ **Not quite right.** Check your output and try again!"

    return Response({
        "is_correct": result["is_correct"],
        "output": result["output"],
        "error": result["error"],
        "friendly_error": friendly_error,
        "test_results": result["test_results"],
        "message": message,
    })


# ════════════════════════════════════════════════════════════
# HEALTH CHECKS
# ════════════════════════════════════════════════════════════

@api_view(["GET"])
@permission_classes([AllowAny])
def root(request):
    return Response({
        "message": "🐍 LearnPython API is running!",
        "docs": "/api/",
        "status": "healthy",
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    return Response({"status": "ok"})
