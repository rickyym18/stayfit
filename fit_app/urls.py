from django.urls import path
from . import views

urlpatterns = [
    path ("", views.login_reg ),
    path("register", views.register),
    path("login", views.login),   
    path("home", views.home_page),
    path("logout", views.logout),
    path("edit/<int:id>", views.edit_workout),
    path("add/workout", views.add_workout),
    path("remove/<int:id>", views.remove_workout),
    path("add/<int:id>", views.add_favorite),
    path("delete/<int:id>", views.delete_workout),
]