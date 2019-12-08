from django.urls import path
from land import views

app_name = 'land'

urlpatterns = [
    path('searchland/', views.landformbuy, name='landformbuy'),
    path('postland/', views.landformsell, name='landformsell'),
    path('add_facility/', views.add_facility, name='add_facility'),

]
