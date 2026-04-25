from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("launch/", views.launch_system, name='launch'),
    path('login/', views.login_forms, name='login'),
    path('logout/', views.logout_forms, name='logout'),
    path('register/', views.register_form, name='register'),
    path('view-records/<int:pk>/', views.view_record, name='view-record'),
]
