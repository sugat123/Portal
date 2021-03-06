from django.urls import path
from jobs import views

app_name = 'jobs'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add_job/', views.add_job, name='add_job'),
    path('add_facility/', views.add_facility, name='add_facility'),
    path('<slug>/post_job/', views.post_job, name='post_job'),
    path('<slug>/apply_job/', views.apply_job, name='apply_job'),
    path('<slug>/job_list/', views.job_list, name='job_list'),
    path('<slug>/posted_job_detail/<int:id>/',
         views.posted_job_detail, name='posted_job_detail'),
    path('<slug>/applied_job_detail/<int:id>/',
         views.applied_job_detail, name='applied_job_detail'),
    path('<slug>/list_job/', views.list_job, name='list_job'),
    path('add_skill/', views.add_skill, name='add_skill'),
    #     path('match/', views.match, name='match'),
    path('khalti/<int:id>', views.khalti, name='khalti'),
    path('search/', views.SearchView.as_view(), name='search'),
]