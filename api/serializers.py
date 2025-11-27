from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import (
    AppUser, WaterLog, WaterSettings,
    ExerciseLog, ExerciseSettings,
    Habit, HabitLog, Achievement, UserAchievement
)

# ---------------------------
# USERS
# ---------------------------
class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


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
        fields = ["id", "code", "title", "description", "icon", "color", "goal"]


class UserAchievementSerializer(serializers.ModelSerializer):
    # para retornar os dados completos da conquista
    achievement = AchievementSerializer(read_only=True)
    # para receber só o id na criação/atualização
    achievement_id = serializers.PrimaryKeyRelatedField(
        queryset=Achievement.objects.all(),
        source="achievement",
        write_only=True
    )

    class Meta:
        model = UserAchievement
        fields = [
            "id",
            "user",
            "achievement",
            "achievement_id",
            "unlocked",
            "progress",
            "unlocked_date",
        ]