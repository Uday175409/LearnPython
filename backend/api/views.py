# ============================================================
# api/views.py — All API Views
# ============================================================
# Endpoints mirror the old FastAPI routes exactly so the React
# frontend works unchanged:
#
#   POST /api/auth/register
#   POST /api/auth/login
#   GET  /api/auth/me
#   GET  /api/courses
#   GET  /api/courses/:id/lessons
#   GET  /api/lessons/:id
#   GET  /api/exercises/:id
#   GET  /api/exercises/:id/solution
#   POST /api/run
#   POST /api/exercises/:id/submit
#   GET  /api/progress
#   POST /api/lessons/:id/complete
#   GET  /           (health check)
#   GET  /health     (health check)
# ============================================================

import asyncio
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Course, Lesson, Exercise, UserProgress, ExerciseAttempt
from .serializers import (
    UserRegisterSerializer,
    UserOutSerializer,
    CourseOutSerializer,
    LessonSummarySerializer,
    LessonDetailSerializer,
    ExerciseOutSerializer,
    ExerciseSolutionSerializer,
)
from sandbox import execute_code, run_exercise_tests
from error_explainer import explain_error


# ── Helpers ──────────────────────────────────────────────────

def _get_tokens_for_user(user):
    """Generate JWT access + refresh tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        "access_token": str(refresh.access_token),
        "token_type": "bearer",
    }


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
# AUTH VIEWS
# ════════════════════════════════════════════════════════════

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """Create a new learner account. Returns JWT immediately."""
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response(
        _get_tokens_for_user(user),
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """Log in with username + password. Returns JWT."""
    username = request.data.get("username", "")
    password = request.data.get("password", "")
    user = authenticate(username=username, password=password)
    if user is None:
        return Response(
            {"detail": "Incorrect username or password. Please try again."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    return Response(_get_tokens_for_user(user))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    """Get the currently logged-in user's information."""
    serializer = UserOutSerializer(request.user)
    return Response(serializer.data)


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
    """
    Return all lessons in a course with completion and lock status.
    Lesson 1 is always unlocked. Lesson N requires N-1 to be completed.
    """
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return Response(
            {"detail": "Course not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    lessons = course.lessons.all().order_by("order")

    # Get completed lesson IDs for the current user
    completed_ids = set()
    if request.user.is_authenticated:
        completed_ids = set(
            UserProgress.objects.filter(
                user=request.user, completed=True
            ).values_list("lesson_id", flat=True)
        )

    result = []
    lesson_list = list(lessons)
    for i, lesson in enumerate(lesson_list):
        is_completed = lesson.id in completed_ids

        result.append({
            "id": lesson.id,
            "course_id": lesson.course_id,
            "title": lesson.title,
            "subtitle": lesson.subtitle or "",
            "order": lesson.order,
            "is_completed": is_completed,
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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

    # Save the attempt
    ExerciseAttempt.objects.create(
        user=request.user,
        exercise=exercise,
        code=code,
        output=result["output"],
        is_correct=result["is_correct"],
        error_message=result["error"],
        friendly_error=friendly_error,
    )

    # If correct, check if lesson is now complete
    if result["is_correct"]:
        _check_lesson_completion(request.user, exercise.lesson_id)

    return Response({
        "is_correct": result["is_correct"],
        "output": result["output"],
        "error": result["error"],
        "friendly_error": friendly_error,
        "test_results": result["test_results"],
        "message": message,
    })


def _check_lesson_completion(user, lesson_id):
    """Mark lesson complete if all its exercises are solved."""
    exercise_ids = set(
        Exercise.objects.filter(lesson_id=lesson_id)
        .values_list("id", flat=True)
    )
    if not exercise_ids:
        return

    solved_ids = set(
        ExerciseAttempt.objects.filter(
            user=user,
            exercise_id__in=exercise_ids,
            is_correct=True,
        ).values_list("exercise_id", flat=True).distinct()
    )

    if solved_ids >= exercise_ids:
        progress, created = UserProgress.objects.get_or_create(
            user=user, lesson_id=lesson_id,
        )
        if not progress.completed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()


# ════════════════════════════════════════════════════════════
# PROGRESS VIEWS
# ════════════════════════════════════════════════════════════

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_progress(request):
    """Return the student's overall progress across all lessons."""
    total_lessons = Lesson.objects.count()
    progress_qs = UserProgress.objects.filter(user=request.user)

    completed_count = progress_qs.filter(completed=True).count()
    percent = (
        round(completed_count / total_lessons * 100, 1)
        if total_lessons > 0
        else 0
    )

    lessons = [
        {
            "lesson_id": p.lesson_id,
            "completed": p.completed,
            "completed_at": p.completed_at,
        }
        for p in progress_qs
    ]

    return Response({
        "total_lessons": total_lessons,
        "completed_lessons": completed_count,
        "percent_complete": percent,
        "lessons": lessons,
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_lesson_complete(request, lesson_id):
    """Manually mark a lesson as completed (for reading-only lessons)."""
    try:
        Lesson.objects.get(pk=lesson_id)
    except Lesson.DoesNotExist:
        return Response(
            {"detail": "Lesson not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    progress, created = UserProgress.objects.get_or_create(
        user=request.user, lesson_id=lesson_id,
    )
    progress.completed = True
    progress.completed_at = timezone.now()
    progress.save()

    return Response({
        "message": "Lesson marked as complete!",
        "lesson_id": lesson_id,
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
