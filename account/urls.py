from django.urls import path
from account.views import *
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    #     path('send-reset-password-email/', SendPasswordResetEmailView.as_view(),
    #          name='send-reset-password-email'),
    #     path('reset-password/<uid>/<token>/',
    #          UserPasswordResetView.as_view(), name='reset-password'),
    path('attendance/', UserTblAttendanceView.as_view(), name='attendance'),
    path('usersites/', UserSitesView.as_view(), name='usersites'),
]
