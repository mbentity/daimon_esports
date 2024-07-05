"""
URL configuration for daimon_esports project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from daimon_esports_app import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', views.Auth.as_view(), name='auth'),
    path('admin/', admin.site.urls),
    path('users/', views.UserList.as_view()),
    path('users/<str:pk>/', views.UserDetail.as_view()),
    path('disciplines/', views.DisciplineList.as_view()),
    path('disciplines/<str:pk>/', views.DisciplineDetail.as_view()),
    path('tournaments/', views.TournamentList.as_view()),
    path('tournaments/<str:pk>/', views.TournamentDetail.as_view()),
    path('tournaments/', views.TournamentSearch.as_view(), name='tournament_search'),
    path('rosters/', views.RosterList.as_view()),
    path('rosters/<str:pk>/', views.RosterDetail.as_view()),
    path('games/', views.GameList.as_view()),
    path('games/<str:pk>/', views.GameDetail.as_view()),
    path('players/', views.PlayerList.as_view()),
    path('players/<str:pk>/', views.PlayerDetail.as_view()),
    path('requests/', views.RequestList.as_view()),
    path('requests/<str:pk>/', views.RequestDetail.as_view()),
]
