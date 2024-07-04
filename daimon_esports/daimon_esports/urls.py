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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.UserList.as_view()),
    path('users/<str:pk>/', views.UserDetail.as_view()),
    path('disciplines/', views.DisciplineList.as_view()),
    path('disciplines/<str:pk>/', views.DisciplineDetail.as_view()),
    path('tournaments/', views.TournamentList.as_view()),
    path('tournaments/<str:pk>/', views.TournamentDetail.as_view()),
    path('rosters/', views.RosterList.as_view()),
    path('rosters/<str:pk>/', views.RosterDetail.as_view()),
    path('games/', views.GameList.as_view()),
    path('games/<str:pk>/', views.GameDetail.as_view()),
    path('players/', views.PlayerList.as_view()),
    path('players/<str:pk>/', views.PlayerDetail.as_view()),
    path('requests/', views.RequestList.as_view()),
    path('requests/<str:pk>/', views.RequestDetail.as_view()),
]
