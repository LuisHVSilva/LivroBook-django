from django.urls import path

from .views import LoginView, UserRegisterView, UserConfirmView, PasswordResetView, CustomPasswordResetConfirmView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('register', UserRegisterView.as_view(), name="register"),
    path('confirm/<int:pk>', UserConfirmView.as_view(), name='confirm'),
    path('password-reset', PasswordResetView.as_view(), name="password_reset"),
    path('password-reset/confirm/<str:uidb64>/<str:token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm')
]
