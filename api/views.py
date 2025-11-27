from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication



from .models import (
    AppUser, WaterLog, WaterSettings,
    ExerciseLog, ExerciseSettings,
    Habit, HabitLog, Achievement, UserAchievement
)
from .serializers import (
    AppUserSerializer, WaterLogSerializer, WaterSettingsSerializer,
    ExerciseLogSerializer, ExerciseSettingsSerializer,
    HabitSerializer, HabitLogSerializer,
    AchievementSerializer, UserAchievementSerializer
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
        except AppUser.DoesNotExist:
            return Response({"detail": "User not found"}, status=404)

        # Água
        water_logs = WaterLog.objects.filter(user_id=user.id)
        total_ml = sum(w.amount_ml for w in water_logs)

        # Exercício
        exercise_logs = ExerciseLog.objects.filter(user_id=user.id)
        total_min = sum(e.duration_min for e in exercise_logs)

        # Hábitos
        habits_total = Habit.objects.filter(user_id=user.id).count()
        habits_done_today = HabitLog.objects.filter(user_id=user.id).count()

        # Conquistas (agora por usuário)
        user_achievements = UserAchievement.objects.filter(user_id=user.id)
        unlocked_count = user_achievements.filter(unlocked=True).count()

        return Response({
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
            },
            "water": {
                "total_logs": water_logs.count(),
                "total_ml": total_ml,
            },
            "exercise": {
                "total_logs": exercise_logs.count(),
                "total_minutes": total_min,
            },
            "habits": {
                "total": habits_total,
                "completed_today": habits_done_today,
            },
            "achievements": {
                "total": user_achievements.count(),
                "unlocked": unlocked_count,
            }
        })


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



from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import AppUser, WaterLog, ExerciseLog, Habit, HabitLog, Achievement

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dashboard_summary(request, user_id):

    try:
        user = AppUser.objects.get(id=user_id)
    except AppUser.DoesNotExist:
        return Response(
            {"detail": "User not found", "code": "user_not_found"},
            status=404
        )

    ensure_user_achievements(user_id)

    water_logs = WaterLog.objects.filter(user_id=user_id)
    ex_logs = ExerciseLog.objects.filter(user_id=user_id)

    habits_count = Habit.objects.filter(user_id=user_id).count()
    habits_today = HabitLog.objects.filter(user_id=user_id).count()

    ua_qs = UserAchievement.objects.filter(user_id=user_id)

    return Response({
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
        "water": {
            "logs": water_logs.count(),
            "total_ml": sum(w.amount_ml for w in water_logs),
        },
        "exercise": {
            "logs": ex_logs.count(),
            "total_min": sum(e.duration_min for e in ex_logs),
        },
        "habits": {
            "count": habits_count,
            "completed_today": habits_today,
        },
        "achievements": {
            "total": ua_qs.count(),
            "unlocked": ua_qs.filter(unlocked=True).count(),
        }
    })
    
    
class UserAchievementViewSet(viewsets.ModelViewSet):
    queryset = UserAchievement.objects.all()
    serializer_class = UserAchievementSerializer
    
    
    
def ensure_user_achievements(user_id: int):
    """Garante que o usuário tenha um UserAchievement para cada Achievement existente."""
    for ach in Achievement.objects.all():
        UserAchievement.objects.get_or_create(
            user_id=user_id,
            achievement=ach,
        )

