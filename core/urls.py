from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('movie/<str:pk>/', views.movie, name='movie'),
    path('my-list', views.my_list, name='my-list'),
    path('add-to-list/', views.add_to_list, name='add-to-list'),

]
