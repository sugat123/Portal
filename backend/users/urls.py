from django.urls import path
from users import views

app_name = 'users'
urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),


]
