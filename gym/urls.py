from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),               # List members
    path('add/', views.add_member, name='add_member'),       # Add member
    path('edit/<int:id>/', views.edit_member, name='edit_member'),   # Edit
    path('delete/<int:id>/', views.delete_member, name='delete_member'), # Delete
]
