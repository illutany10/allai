from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import requests
import json


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


class GitHubOAuthView(APIView):
    """
    GitHub OAuth 로그인 처리
    """
    permission_classes = [AllowAny]

    def post(self, request):
        access_token = request.data.get("access_token")
        
        if not access_token:
            return Response(
                {"error": "GitHub access token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # GitHub API에서 사용자 정보 가져오기
            headers = {
                "Authorization": f"token {access_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            response = requests.get("https://api.github.com/user", headers=headers)
            
            if response.status_code != 200:
                return Response(
                    {"error": "Invalid GitHub access token"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            
            github_user = response.json()
            github_id = github_user.get("id")
            github_username = github_user.get("login")
            github_email = github_user.get("email")
            github_name = github_user.get("name", "")
            
            # GitHub ID로 기존 사용자 찾기 (username에 github_ prefix 사용)
            username = f"github_{github_username}"
            
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # 새 사용자 생성
                user = User.objects.create_user(
                    username=username,
                    email=github_email or f"{github_username}@github.local",
                    first_name=github_name.split(" ")[0] if github_name else github_username,
                    last_name=" ".join(github_name.split(" ")[1:]) if github_name and " " in github_name else "",
                )
                # GitHub ID를 저장하기 위해 Profile 모델이 있다면 추가 가능
            
            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            
            return Response(
                {
                    "message": "GitHub login successful",
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
            
        except requests.RequestException:
            return Response(
                {"error": "Failed to fetch GitHub user data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
