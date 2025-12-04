from django.db import models
from django.contrib.auth.models import User


# -------------------------
# USERS
# -------------------------
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class AppUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("O usuário precisa de um e-mail")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    # Campos obrigatórios para qualquer usuário Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AppUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

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
    goal = models.IntegerField(default=1)  # quantos eventos precisa p/ concluir

    def __str__(self):
        return self.title


class UserAchievement(models.Model):
    user = models.ForeignKey("AppUser", on_delete=models.CASCADE, related_name="user_achievements")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name="user_achievements")

    unlocked = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)
    unlocked_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.name} - {self.achievement.title}"