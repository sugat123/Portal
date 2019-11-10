from django.urls import path
from room import views

app_name = 'room'

urlpatterns = [
    path('', views.roomtype, name='roomtype'),
    path('<int:roomtype_id>/roomlist/', views.roomlist, name='roomlist'),
    path('<int:roomtype_id>/roomlist/findroom/', views.findroom, name='findroom'),
    path('<int:roomtype_id>/roomlist/postroom/', views.postroom, name='postroom'),
    path('add_facility/', views.add_facility, name='add_facility'),
]