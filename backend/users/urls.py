from django.urls import path, reverse_lazy
from users import views
from django.contrib.auth import views as auth_views

app_name = 'users'
urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('activation/', views.check_activation_code, name='activation'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html', email_template_name='users/password_reset_email.html',
        success_url=reverse_lazy('users:password_reset_done', ), from_email="DJ Group <settings.EMAIL_HOST_USER>",), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html', ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html', success_url=reverse_lazy('users:password_reset_complete', ),),
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html',), name='password_reset_complete'),
]
