from django.db import models
from django.contrib.auth.models import User


# -------------------------
# USERS
# -------------------------
class AppUser(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# -------------------------
# WATER
# -------------------------
class WaterLog(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    amount_ml = models.IntegerField()
    timestamp_ms = models.BigIntegerField()

    def __str__(self):
        return f"{self.user.name} - {self.amount_ml}ml"


class WaterSettings(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    daily_goal_ml = models.IntegerField(default=2000)

    def __str__(self):
        return f"{self.user.name} - Meta {self.daily_goal_ml} ml"


# -------------------------
# EXERCISES
# -------------------------
class ExerciseLog(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    intensity = models.CharField(max_length=50)
    duration_min = models.IntegerField()
    timestamp_ms = models.BigIntegerField()

    def __str__(self):
        return f"{self.user.name} - {self.type}"


class ExerciseSettings(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    daily_goal_min = models.IntegerField(default=30)

    def __str__(self):
        return f"{self.user.name} - Meta treino {self.daily_goal_min} min"


# -------------------------
# HABITS
# -------------------------
class Habit(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    streak = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.name} - {self.name}"


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    timestamp_ms = models.BigIntegerField()
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.habit.name} - log"


# -------------------------
# ACHIEVEMENTS
# -------------------------
class Achievement(models.Model):
    code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    unlocked = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)
    goal = models.IntegerField(default=1)
    unlocked_date = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title
