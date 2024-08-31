from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from daimon_esports_app import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('', views.index, name='index'),
    path('user/', views.UserView.as_view(), name='user'),
    path('user/register/', views.UserRegister.as_view(), name='user-register'),
    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/name/', views.UserName.as_view(), name='user-name'),
    path('user/username/', views.UserUserName.as_view(), name='user-username'),
    path('user/password/', views.UserPassword.as_view(), name='user-password'),
    path('user/teams/', views.UserTeams.as_view(), name='user-teams'),
    path('user/tournaments/', views.UserTournaments.as_view(), name='user-tournaments'),
    path('user/requests/in/', views.UserRequestsIn.as_view(), name='user-requests-in'),
    path('user/requests/out/', views.UserRequestsIn.as_view(), name='user-requests-out'),
    path('disciplines/', views.DisciplineList.as_view(), name='discipline-list'),
    path('tournaments/search/', views.TournamentSearch.as_view(), name='tournament-search'),
    path('tournaments/create/', views.TournamentCreate.as_view(), name='tournament-create'),
    path('tournaments/<str:pk>/', views.TournamentDetail.as_view(), name='tournament-detail'),
    path('tournaments/<str:pk>/name/', views.TournamentName.as_view(), name='tournament-update-name'),
    path('tournaments/<str:pk>/discipline/', views.TournamentDiscipline.as_view(), name='tournament-update-discipline'),
    path('tournaments/<str:pk>/stream/', views.TournamentStream.as_view(), name='tournament-update-stream'),
    path('tournaments/<str:pk>/meet/', views.TournamentMeet.as_view(), name='tournament-update-meet'),
    path('tournaments/<str:pk>/dates/', views.TournamentDates.as_view(), name='tournament-update-dates'),
    path('tournaments/<str:pk>/cansubscribe/', views.TournamentCanSubscribe.as_view(), name='tournament-cansubscribe'),
    path('teams/create/', views.TeamCreate.as_view(), name='team-create'),
    path('teams/<str:pk>/', views.TeamDetail.as_view(), name='team-detail'),
    path('teams/<str:pk>/transferownership/', views.TeamTransferOwnership.as_view(), name='team-transfer-ownership'),
    path('teams/<str:pk>/logo/', views.TeamLogo.as_view(), name='team-logo'),
    path('games/', views.GameList.as_view(), name='game-list'),
    path('games/<str:pk>/', views.GameDetail.as_view(), name='game-detail'),
    path('games/<str:pk>/teams/', views.GameTeams.as_view(), name='game-teams'),
    path('games/<str:pk>/score/', views.GameScore.as_view(), name='game-score'),
    path('games/<str:pk>/time/', views.GameTime.as_view(), name='game-time'),
    path('games/<str:pk>/minutes/', views.GameMinutes.as_view(), name='game-minutes'),
    path('players/<str:pk>/', views.PlayerDetail.as_view(), name='player-detail'),
    path('requests/create/', views.RequestCreate.as_view(), name='request-create'),
    path('requests/accept/', views.RequestAccept.as_view(), name='request-accept'),
    path('requests/<str:pk>/', views.RequestDetail.as_view(), name='request-detail'),
    path('admin/', admin.site.urls, name='admin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)