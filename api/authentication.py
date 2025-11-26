from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import AppUser


class AppLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = AppUser.objects.get(email=email)
        except AppUser.DoesNotExist:
            return Response({"detail": "Usuário não encontrado"}, status=404)

        # Aqui, como sua senha não está criptografada, compare direto:
        if user.password != password:
            return Response({"detail": "Senha incorreta"}, status=400)

        # Gerar token manualmente
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
        })
