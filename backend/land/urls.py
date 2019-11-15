from django.urls import path
from land import views

app_name = 'land'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
   
]