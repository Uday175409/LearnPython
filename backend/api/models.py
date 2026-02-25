# ============================================================
# api/models.py — Database Models
# ============================================================
# Uses Django's built-in User model for authentication.
# Custom models for Course, Lesson, Exercise, Progress.
# ============================================================

from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    """A course groups related lessons together."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)
    icon = models.CharField(max_length=50, default="📘")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """One lesson teaches ONE concept."""
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons"
    )
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True, default="")
    content_blocks = models.JSONField(default=list)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"


class Exercise(models.Model):
    """A hands-on practice problem attached to a lesson."""
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("challenge", "Challenge"),
    ]

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="exercises"
    )
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    starter_code = models.TextField(blank=True, default="")
    hint = models.TextField(blank=True, default="")
    solution = models.TextField(blank=True, default="")
    explanation = models.TextField(blank=True, default="")
    tests = models.JSONField(default=list)
    order = models.IntegerField(default=0)
    difficulty = models.CharField(
        max_length=20, choices=DIFFICULTY_CHOICES, default="easy"
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class UserProgress(models.Model):
    """Tracks which lessons a user has completed."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="progress"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="progress"
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "lesson")

    def __str__(self):
        return f"{self.user.username} — {self.lesson.title}"


class ExerciseAttempt(models.Model):
    """Records every code submission a student makes."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="attempts"
    )
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name="attempts"
    )
    code = models.TextField()
    output = models.TextField(blank=True, default="")
    is_correct = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, default="")
    friendly_error = models.TextField(blank=True, default="")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "✅" if self.is_correct else "❌"
        return f"{status} {self.user.username} → {self.exercise.title}"
