from django.urls import path
from jobs import views

app_name = 'jobs'

urlpatterns = [
    path('', views.index, name='index'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_job/', views.add_job, name='add_job'),
    path('add_facility/', views.add_facility, name='add_facility'),
    path('<slug>/post_job/', views.post_job, name='post_job'),
    path('<slug>/apply_job/', views.apply_job, name='apply_job'),
    path('<slug>/list_job/', views.list_job, name='list_job'),
    path('add_skill/', views.add_skill, name='add_skill')

]
