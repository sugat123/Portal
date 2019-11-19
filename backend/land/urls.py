from django.urls import path
from land import views

app_name = 'land'

urlpatterns = [
    path('', views.landform, name='landform'),
   
]