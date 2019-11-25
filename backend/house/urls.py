from django.urls import path
from house import views

app_name = 'house'

urlpatterns=[

    path('', views.owner, name='owner'),
    path('buyer', views.buyer, name='buyer'),
    # path('', views.sekker, name='sekker'),
    path('house_list/', views.house_list, name='house_list'),
    path('house_list/house/<int:id>/', views.sellerhouse_detail , name='sellerhouse_detail'),
    path('house_list/home/<int:id>/', views.buyerhouse_detail , name='buyerhouse_detail'),
    path('add_facility/', views.add_facility , name='add_facility')
]