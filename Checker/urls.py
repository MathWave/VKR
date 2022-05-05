from django.urls import path

from Checker import views

urlpatterns = [
    path("status", views.status),
    path("available", views.available),
    path("get_dynamic", views.get_dynamic),
    path("save_solution", views.save_solution),
    path("save_progress", views.save_progress),
    path("notify", views.notify)
]
