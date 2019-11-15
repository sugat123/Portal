from django.urls import path
from room import views

app_name = 'room'

urlpatterns = [
    path('', views.roomtype, name='roomtype'),
    path('<int:roomtype_id>/roomlist/', views.roomlist, name='roomlist'),
    path('<int:roomtype_id>/roomlist/searchroom/', views.searchroom, name='searchroom'),
    path('<int:roomtype_id>/roomlist/postroom/', views.postroom, name='postroom'),
    path('add_facility/', views.add_facility, name='add_facility'),
    path('<str:user_type>/room detail/<int:room_id>', views.detail, name='detail')
]