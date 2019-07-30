from django.urls import path
from jobs import views

app_name = 'jobs'

urlpatterns = [
    path('index/', views.index, name='index'),
]
