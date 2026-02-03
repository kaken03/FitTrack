from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),               # List members
    path('add/', views.add_member, name='add_member'),       # Add member
    path('edit/<int:id>/', views.edit_member, name='edit_member'),   # Edit
    path('delete/<int:id>/', views.delete_member, name='delete_member'), # Delete
    # Plan management
    path('plans/add/', views.add_plan, name='add_plan'),
    path('plans/edit/<int:id>/', views.edit_plan, name='edit_plan'),
    path('plans/delete/<int:id>/', views.delete_plan, name='delete_plan'),
]
