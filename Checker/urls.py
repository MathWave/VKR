from django.urls import path

from Checker import views

urlpatterns = [
    path("status", views.status),
    path("available", views.available),
    path("get_dynamic", views.get_dynamic),
    path("set_result", views.set_result),
    path("current_test", views.current_test),
]
