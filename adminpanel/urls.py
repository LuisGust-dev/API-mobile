from django.urls import path
from .views import (
    logout_view, panel_login, dashboard,

    # Users
    users_page, user_details, user_edit, user_delete,

    # Habits
    habits_list, habit_create, habit_edit, habit_delete,

    # Achievements
    achievements_list, achievement_create, achievement_edit, achievement_delete,

    # Water
    water_list, water_create, water_edit, water_delete,

    # Exercise
    exercise_list, exercise_edit, exercise_delete,
)

urlpatterns = [
    path("login/", panel_login, name="panel_login"),
    path("", dashboard, name="dashboard"),
    path("logout/", logout_view, name="logout"),

    # USERS
    path("users/", users_page, name="users_page"),
    path("users/<int:user_id>/", user_details, name="user_details"),
    path("users/<int:user_id>/edit/", user_edit, name="user_edit"),
    path("users/<int:user_id>/delete/", user_delete, name="user_delete"),

    # HABITS
    path("habits/", habits_list, name="habits_list"),
    path("habits/create/", habit_create, name="habit_create"),
    path("habits/<int:habit_id>/edit/", habit_edit, name="habit_edit"),
    path("habits/<int:habit_id>/delete/", habit_delete, name="habit_delete"),

    # ACHIEVEMENTS
    path("achievements/", achievements_list, name="achievements_list"),
    path("achievements/create/", achievement_create, name="achievement_create"),
    path("achievements/<int:ach_id>/edit/", achievement_edit, name="achievement_edit"),
    path("achievements/<int:ach_id>/delete/", achievement_delete, name="achievement_delete"),
    
    # WATER
    path("water/", water_list, name="water_list"),
    path("water/create/", water_create, name="water_create"),
    path("water/<int:log_id>/edit/", water_edit, name="water_edit"),
    path("water/<int:log_id>/delete/", water_delete, name="water_delete"),
    
    
    # EXERCISE
    path("exercise/", exercise_list, name="exercise_list"),
    path("exercise/<int:log_id>/edit/", exercise_edit, name="exercise_edit"),
    path("exercise/<int:log_id>/delete/", exercise_delete, name="exercise_delete"),

]
