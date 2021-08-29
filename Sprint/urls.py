from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from Main.views import *
from Sprint import settings

urlpatterns = [
    path("enter", EnterView.as_view()),
    path("register", RegisterView.as_view()),
    path("rating", RatingView.as_view()),
    path("tasks", TasksView.as_view()),
    path("account", AccountView.as_view()),
    path("exit", ExitView.as_view()),
    path("admin/task", TaskSettingsView.as_view()),
    path("sets", SetsView.as_view()),
    path("task", TaskView.as_view()),
    path("solutions_table", SolutionsTableView.as_view()),
    path("", MainView.as_view()),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
