from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password, make_password
from .models import AppUser  # <-- usa seu modelo customizado

class AppLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = AppUser.objects.get(email=email)
        except AppUser.DoesNotExist:
            return Response({"detail": "Usuário não encontrado"}, status=404)

        # senha criptografada
        if not check_password(password, user.password):
            return Response({"detail": "Senha incorreta"}, status=400)

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
        })


class AppRegisterView(APIView):
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")

        if AppUser.objects.filter(email=email).exists():
            return Response({"detail": "E-mail já cadastrado!"}, status=400)

        # cria com senha criptografada
        user = AppUser.objects.create(
            name=name,
            email=email,
            password=make_password(password)
        )

        return Response({
            "message": "Usuário criado com sucesso!",
            "user_id": user.id,
        }, status=201)
