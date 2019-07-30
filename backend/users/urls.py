from django.urls import path
from users import views

app_name = 'users'
urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register, name='register'),
    path('logut/', views.logout_user, name='logout'),


]
