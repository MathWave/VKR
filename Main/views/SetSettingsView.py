import datetime
from typing import Optional

import pytz
from django.utils import timezone

from Main.models import SetTask, Set
from SprintLib.BaseView import BaseView, AccessError


class SetSettingsView(BaseView):
    required_login = True
    view_file = "set_settings.html"
    endpoint = "admin/set"
    current_set: Optional[Set] = None

    def pre_handle(self):
        self.current_set = self.entities.set
        if (
            self.request.user != self.current_set.creator
            and self.request.user.username not in self.current_set.editors
        ):
            raise AccessError()

    def get(self):
        self.context["settasks"] = SetTask.objects.filter(
            set=self.current_set
        ).order_by("name")
        self.context["start_time"] = (
            self.current_set.start_time_format
            if self.current_set.start_time
            else timezone.now().strftime("%Y-%m-%dT%H:%M")
        )
        self.context["end_time"] = (
            self.current_set.end_time_format
            if self.current_set.end_time
            else timezone.now().strftime("%Y-%m-%dT%H:%M")
        )

    def post_save(self):
        for key, value in self.request.POST.items():
            if key.startswith("settask_"):
                st = SetTask.objects.get(id=key.split("_")[1])
                st.name = value
                st.save()
        self.current_set.name = self.request.POST["name"]
        self.current_set.description = self.request.POST['description']
        self.current_set.save()
        return "/admin/set?set_id=" + str(self.current_set.id)

    def post_edit(self):
        current_tasks = self.entities.set.tasks
        task_ids = [task.id for task in current_tasks]
        for key, value in self.request.POST.items():
            if key.startswith("task_"):
                i = int(key.split("_")[1])
                if i not in task_ids:
                    SetTask.objects.create(set=self.entities.set, task_id=i)
        to_delete = [i for i in task_ids if "task_" + str(i) not in self.request.POST]
        SetTask.objects.filter(task_id__in=to_delete).delete()
        return "/admin/set?set_id=" + str(self.entities.set.id)

    def post_time(self):
        try:
            tz = pytz.timezone("Europe/Moscow")
            if "start_time_check" in self.request.POST:
                self.current_set.start_time = None
            else:
                self.current_set.start_time = tz.localize(
                    datetime.datetime.strptime(
                        self.request.POST["start_time"], "%Y-%m-%dT%H:%M"
                    )
                )
            if "end_time_check" in self.request.POST:
                self.current_set.end_time = None
            else:
                self.current_set.end_time = tz.localize(
                    datetime.datetime.strptime(
                        self.request.POST["end_time"], "%Y-%m-%dT%H:%M"
                    )
                )
            self.current_set.opened = 'opened' in self.request.POST.keys()
            self.current_set.public = 'public' in self.request.POST.keys()
        except ValueError:
            return "/admin/set?set_id=" + str(self.current_set.id)
        self.current_set.save()
        return "/admin/set?set_id=" + str(self.current_set.id)
