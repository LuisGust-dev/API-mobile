from django.contrib import admin
from .models import (
    AppUser, WaterLog, WaterSettings,
    ExerciseLog, ExerciseSettings,
    Habit, HabitLog,
    Achievement
)

admin.site.register(AppUser)
admin.site.register(WaterLog)
admin.site.register(WaterSettings)
admin.site.register(ExerciseLog)
admin.site.register(ExerciseSettings)
admin.site.register(Habit)
admin.site.register(HabitLog)
admin.site.register(Achievement)
