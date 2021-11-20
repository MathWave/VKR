from django.contrib import admin
from django.urls import path

from Main.views import *

urlpatterns = [
    path("enter", EnterView.as_view()),
    path("rating", RatingView.as_view()),
    path("tasks", TasksView.as_view()),
    path("account", AccountView.as_view()),
    path("exit", ExitView.as_view()),
    path("admin/task", TaskSettingsView.as_view()),
    path("sets", SetsView.as_view()),
    path("task", TaskView.as_view()),
    path("solution", SolutionView.as_view()),
    path("solutions_table", SolutionsTableView.as_view()),
    path("task_runtime", TaskRuntimeView.as_view()),
    path("image", ImageView.as_view()),
    path("send_code", SendCodeView.as_view()),
    path("", MainView.as_view()),
    path("admin/", admin.site.urls),
]
