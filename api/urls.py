from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .authentication import AppLoginView, AppRegisterView

from .views import (
    AppUserViewSet, WaterLogViewSet, WaterSettingsViewSet,
    ExerciseLogViewSet, ExerciseSettingsViewSet,
    HabitViewSet, HabitLogViewSet,
    AchievementViewSet, UserAchievementViewSet,
    dashboard_summary
)

router = DefaultRouter()

# USERS
router.register(r'users', AppUserViewSet)

# WATER
router.register(r'water/logs', WaterLogViewSet)
router.register(r'water/settings', WaterSettingsViewSet)

# EXERCISE
router.register(r'exercise/logs', ExerciseLogViewSet)
router.register(r'exercise/settings', ExerciseSettingsViewSet)

# HABITS
router.register(r'habits', HabitViewSet)
router.register(r'habit/logs', HabitLogViewSet)

# ACHIEVEMENTS
router.register(r'achievements', AchievementViewSet)

# USER ACHIEVEMENTS
router.register(r'user-achievements', UserAchievementViewSet)

urlpatterns = [
    #  LOGIN
    path('login/', AppLoginView.as_view(), name='api-login'),

    #  REGISTER (NOVA ROTA)
    path('register/', AppRegisterView.as_view(), name='api-register'),

    # ROUTER (CRUDs)
    path('', include(router.urls)),

    # DASHBOARD SUMMARY
    path('dashboard/<int:user_id>/', dashboard_summary),
]
