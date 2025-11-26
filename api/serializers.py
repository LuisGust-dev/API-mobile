from rest_framework import serializers
from .models import (
    AppUser, WaterLog, WaterSettings,
    ExerciseLog, ExerciseSettings,
    Habit, HabitLog, Achievement
)

# ---------------------------
# USERS
# ---------------------------
class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = '__all__'


# ---------------------------
# WATER
# ---------------------------
class WaterLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterLog
        fields = '__all__'


class WaterSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterSettings
        fields = '__all__'


# ---------------------------
# EXERCISES
# ---------------------------
class ExerciseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseLog
        fields = '__all__'


class ExerciseSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSettings
        fields = '__all__'


# ---------------------------
# HABITS
# ---------------------------
class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = '__all__'


# ---------------------------
# ACHIEVEMENTS
# ---------------------------
class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'
