from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('refresh/', views.RefreshTokenView.as_view(), name='refresh_token'),
    path('github/', views.GitHubOAuthView.as_view(), name='github_oauth'),
]
