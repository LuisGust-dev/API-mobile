from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    AppUser, WaterLog, WaterSettings,
    ExerciseLog, ExerciseSettings,
    Habit, HabitLog, Achievement
)
from .serializers import (
    AppUserSerializer, WaterLogSerializer, WaterSettingsSerializer,
    ExerciseLogSerializer, ExerciseSettingsSerializer,
    HabitSerializer, HabitLogSerializer,
    AchievementSerializer
)

# USERS
class AppUserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer

    # ===========================
    #   USER STATS ENDPOINT
    #   ROTA: /api/users/<id>/stats/
    # ===========================
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        try:
            user = AppUser.objects.get(pk=pk)

            water_logs = WaterLog.objects.filter(user_id=user.id)
            exercise_logs = ExerciseLog.objects.filter(user_id=user.id)
            habits = Habit.objects.filter(user_id=user.id)
            achievements = Achievement.objects.all()  # global no seu app

            return Response({
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                },
                "water": {
                    "total_logs": water_logs.count(),
                    "total_ml": sum([w.amount_ml for w in water_logs])
                },
                "exercise": {
                    "total_logs": exercise_logs.count(),
                    "total_minutes": sum([e.duration_min for e in exercise_logs])
                },
                "habits": habits.count(),
                "achievements_unlocked": achievements.filter(unlocked=1).count(),
                "achievements_total": achievements.count()
            })

        except AppUser.DoesNotExist:
            return Response({"detail": "User not found"}, status=404)

# WATER
class WaterLogViewSet(viewsets.ModelViewSet):
    queryset = WaterLog.objects.all()
    serializer_class = WaterLogSerializer


class WaterSettingsViewSet(viewsets.ModelViewSet):
    queryset = WaterSettings.objects.all()
    serializer_class = WaterSettingsSerializer


# EXERCISE
class ExerciseLogViewSet(viewsets.ModelViewSet):
    queryset = ExerciseLog.objects.all()
    serializer_class = ExerciseLogSerializer


class ExerciseSettingsViewSet(viewsets.ModelViewSet):
    queryset = ExerciseSettings.objects.all()
    serializer_class = ExerciseSettingsSerializer


# HABITS
class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class HabitLogViewSet(viewsets.ModelViewSet):
    queryset = HabitLog.objects.all()
    serializer_class = HabitLogSerializer


# ACHIEVEMENTS
class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
