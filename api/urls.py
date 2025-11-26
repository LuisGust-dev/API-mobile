from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .authentication import AppLoginView   # <-- IMPORTANTE

from .views import (
    AppUserViewSet, WaterLogViewSet, WaterSettingsViewSet,
    ExerciseLogViewSet, ExerciseSettingsViewSet,
    HabitViewSet, HabitLogViewSet,
    AchievementViewSet
)

router = DefaultRouter()

router.register(r'users', AppUserViewSet)
router.register(r'water/logs', WaterLogViewSet)
router.register(r'water/settings', WaterSettingsViewSet)

router.register(r'exercise/logs', ExerciseLogViewSet)
router.register(r'exercise/settings', ExerciseSettingsViewSet)

router.register(r'habits', HabitViewSet)
router.register(r'habit/logs', HabitLogViewSet)

router.register(r'achievements', AchievementViewSet)

urlpatterns = [
    path('login/', AppLoginView.as_view(), name='api-login'),   # <-- AQUI
    path('', include(router.urls)),
]
