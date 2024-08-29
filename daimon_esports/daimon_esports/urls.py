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
    path('user/', views.UserView.as_view(), name='user'),
    path('user/name/', views.UserName.as_view(), name='user-name'),
    path('user/username/', views.UserUserName.as_view(), name='user-username'),
    path('user/password/', views.UserPassword.as_view(), name='user-password'),
    path('user/register/', views.UserRegister.as_view(), name='user-register'),
    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/logout/', views.UserLogout.as_view(), name='user-logout'),
    path('user/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/authenticated/', views.UserAuthenticated.as_view(), name='user-authenticated'),
    path('user/teams/', views.UserTeams.as_view(), name='user-teams'),
    path('user/tournaments/', views.UserTournaments.as_view(), name='user-tournaments'),
    path('user/requests/', views.UserRequests.as_view(), name='user-requests'),
    path('user/outgoingrequests/', views.UserOutgoingRequests.as_view(), name='user-outgoingrequests'),
    path('users/', views.UserList.as_view()),
    path('users/<str:pk>/', views.UserDetail.as_view()),
    path('disciplines/', views.DisciplineList.as_view()),
    path('disciplines/<str:pk>/', views.DisciplineDetail.as_view()),
    path('tournaments/', views.TournamentList.as_view()),
    path('tournamentscreate/', views.TournamentCreate.as_view(), name='tournament-create'),
    path('tournaments/update/<str:pk>/', views.TournamentUpdate.as_view(), name='tournament-update'),
    path('tournaments/search/', views.TournamentSearch.as_view(), name='tournament-search'),
    path('tournaments/<str:pk>/', views.TournamentDetail.as_view()),
    path('tournaments/<str:pk>/cancreateteam/', views.TournamentCanCreateTeam.as_view(), name='tournament-cancreateteam'),
    path('teams/', views.TeamList.as_view()),
    path('teams/<str:pk>/', views.TeamDetail.as_view()),
    path('games/', views.GameList.as_view()),
    path('games/pop/', views.GamePop.as_view(), name='game-pop'),
    path('games/<str:pk>/', views.GameDetail.as_view()),
    path('players/', views.PlayerList.as_view()),
    path('players/<str:pk>/', views.PlayerDetail.as_view()),
    path('requests/', views.RequestList.as_view()),
    path('requests/<str:pk>/', views.RequestDetail.as_view()),
    path('admin/', admin.site.urls, name='admin'),
]
