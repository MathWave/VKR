from django.urls import path

from Messaging import views

urlpatterns = [
    path("chat_window", views.chat_window),
]
