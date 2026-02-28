# ============================================================
# api/serializers.py — DRF Serializers (No Auth)
# ============================================================
# These define what data the API accepts and returns.
# They match the exact JSON shapes the React frontend expects.
# ============================================================

from rest_framework import serializers
from .models import Course, Lesson, Exercise


# ── Course ───────────────────────────────────────────────────

class CourseOutSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "description", "order", "icon", "lesson_count"]


# ── Lesson ───────────────────────────────────────────────────

class LessonSummarySerializer(serializers.ModelSerializer):
    is_completed = serializers.BooleanField(default=False, read_only=True)
    is_locked = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = Lesson
        fields = [
            "id", "course_id", "title", "subtitle",
            "order", "is_completed", "is_locked",
        ]


class ExerciseOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = [
            "id", "lesson_id", "title", "instructions",
            "starter_code", "hint", "difficulty", "order",
        ]


class LessonDetailSerializer(serializers.ModelSerializer):
    exercises = ExerciseOutSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = [
            "id", "course_id", "title", "subtitle",
            "content_blocks", "order", "exercises",
        ]


class ExerciseSolutionSerializer(serializers.Serializer):
    solution = serializers.CharField()
    explanation = serializers.CharField()
