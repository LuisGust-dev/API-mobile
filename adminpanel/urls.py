from django.urls import path
from .views import panel_login, dashboard, user_details, users_page

urlpatterns = [
    path('login/', panel_login, name='panel_login'),
    path('', dashboard, name='dashboard'),
    path('users/', users_page, name='users_page'),
    path("users/<int:user_id>/", user_details, name="user_details"),

]
