from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginView(APIView):
    """
    사용자 로그인 및 JWT 토큰 발급
    """

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 사용자 인증
        user = authenticate(username=username, password=password)

        if user is not None:
            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "Login successful",
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "user": {
                        "id": user.pk,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class RegisterView(APIView):
    """
    새 사용자 등록
    """

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 사용자 중복 확인
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        if email and User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 새 사용자 생성
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User created successfully",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "user": {
                    "id": user.pk,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class RefreshTokenView(APIView):
    """
    Refresh Token을 사용하여 새로운 Access Token 발급
    """

    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token

            return Response(
                {
                    "access_token": str(access_token),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED
            )
