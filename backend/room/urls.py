from django.urls import path
from room import views

app_name = 'room'

urlpatterns = [
    path('', views.roomtype, name='roomtype'),
    path('<int:roomtype_id>/roomlist/', views.roomlist, name='roomlist'),
    path('<int:roomtype_id>/roomlist/searchroom/', views.searchroom, name='searchroom'),
    path('<int:roomtype_id>/roomlist/postroom/', views.postroom, name='postroom'),
    path('add_facility/', views.add_facility, name='add_facility'),
    path('<int:roomtype_id>/posted_room_detail/<int:id>/', views.posted_room_detail, name='posted_room_detail'),
    path('<int:roomtype_id>/searched_room_detail/<int:id>/', views.searched_room_detail, name='searched_room_detail')

]