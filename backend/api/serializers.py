# ============================================================
# api/serializers.py — DRF Serializers
# ============================================================
# These define what data the API accepts and returns.
# They match the exact JSON shapes the React frontend expects.
# ============================================================

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Course, Lesson, Exercise, UserProgress, ExerciseAttempt


# ── Auth ─────────────────────────────────────────────────────

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=50)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(min_length=6, write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "This username is already taken. Try a different one!"
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists. Try logging in!"
            )
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserOutSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(source="date_joined")

    class Meta:
        model = User
        fields = ["id", "username", "email", "created_at"]


# ── Course ───────────────────────────────────────────────────

class CourseOutSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "order", "icon", "lesson_count"]

    def get_lesson_count(self, obj):
        return obj.lessons.count()


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


# ── Code Execution ───────────────────────────────────────────

class RunCodeRequestSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=5000)


class RunCodeResponseSerializer(serializers.Serializer):
    output = serializers.CharField(allow_blank=True)
    error = serializers.CharField(allow_blank=True, default="")
    friendly_error = serializers.CharField(allow_blank=True, default="")
    execution_time_ms = serializers.IntegerField(default=0)


class SubmitExerciseRequestSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=5000)


class SubmitExerciseResponseSerializer(serializers.Serializer):
    is_correct = serializers.BooleanField()
    output = serializers.CharField(allow_blank=True)
    error = serializers.CharField(allow_blank=True, default="")
    friendly_error = serializers.CharField(allow_blank=True, default="")
    test_results = serializers.ListField(default=[])
    message = serializers.CharField(allow_blank=True, default="")


# ── Progress ─────────────────────────────────────────────────

class ProgressOutSerializer(serializers.ModelSerializer):
    lesson_id = serializers.IntegerField(source="lesson.id")
    completed_at = serializers.DateTimeField()

    class Meta:
        model = UserProgress
        fields = ["lesson_id", "completed", "completed_at"]


class OverallProgressSerializer(serializers.Serializer):
    total_lessons = serializers.IntegerField()
    completed_lessons = serializers.IntegerField()
    percent_complete = serializers.FloatField()
    lessons = ProgressOutSerializer(many=True)
