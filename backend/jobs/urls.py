from django.urls import path
from jobs import views

app_name = 'jobs'

urlpatterns = [
    path('', views.index, name='index'),
    path('giver/', views.giver, name='giver'),
    path('seeker/', views.seeker, name='seeker'),
    path('add_job/', views.add_job, name='add_job'),
    path('<slug>/post_job/', views.post_job, name='post_job'),
    path('<slug>/list_job/', views.list_job, name='list_job'),
    path('add_skill/',views.add_skill, name= 'add_skill')

]
