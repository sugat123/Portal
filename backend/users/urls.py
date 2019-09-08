from django.urls import path
from users import views

app_name = 'users'
urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('activation/', views.check_activation_code, name='activation'),
]
