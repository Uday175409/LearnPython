# ============================================================
# api/models.py — Database Models (No Auth)
# ============================================================
# Simple content models: Course, Lesson, Exercise.
# No user models — the app is fully public.
# ============================================================

from django.db import models


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
