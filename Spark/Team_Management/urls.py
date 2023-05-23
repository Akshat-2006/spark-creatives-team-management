from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('viewall/', views.view_all, name='View_all'),
    path('login', views.sign_in, name='login'),
    path('MyTeam/viewall/user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('viewall/create/', views.create_user, name='create_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user')
]