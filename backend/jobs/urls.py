from django.urls import path
from jobs import views

app_name = 'jobs'

urlpatterns = [
    path('', views.index, name='index'),
    path('giver/', views.giver, name='giver'),
    path('seeker/', views.seeker, name='seeker'),
    path('add_job/', views.add_job, name='add_job'),
    path('<slug>/post_job/', views.post_job, name='post_job'),


]
