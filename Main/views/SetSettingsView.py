import datetime

import pytz
from django.utils import timezone

from Checker.models import Checker
from Main.models import SetTask, Set
from SprintLib.BaseView import BaseView, AccessError
from SprintLib.language import languages


class SetSettingsView(BaseView):
    required_login = True
    view_file = "set_settings.html"
    endpoint = "admin/set"
    set: Set

    def pre_handle(self):
        if (
            self.request.user != self.set.creator
            and self.request.user.username not in self.set.editors
        ):
            raise AccessError()

    def get(self):
        self.context["settasks"] = SetTask.objects.filter(
            set=self.set
        ).order_by("name")
        self.context["start_time"] = (
            self.set.start_time_format
            if self.set.start_time
            else timezone.now().strftime("%Y-%m-%dT%H:%M")
        )
        self.context["end_time"] = (
            self.set.end_time_format
            if self.set.end_time
            else timezone.now().strftime("%Y-%m-%dT%H:%M")
        )
        self.context['languages'] = languages

    def post(self):
        self.set.name = self.request.POST["name"]
        self.set.description = self.request.POST['description']
        self.set.save()
        return "/admin/set?set_id=" + str(self.set.id)

    def post_save(self):
        for key, value in self.request.POST.items():
            if key.startswith("settask_"):
                st = SetTask.objects.get(id=key.split("_")[1])
                st.name = value
                st.save()
        return "/admin/set?set_id=" + str(self.set.id)

    def post_edit(self):
        current_tasks = self.set.tasks
        task_ids = [task.id for task in current_tasks]
        for key, value in self.request.POST.items():
            if key.startswith("task_"):
                i = int(key.split("_")[1])
                if i not in task_ids:
                    SetTask.objects.create(set=self.set, task_id=i)
        to_delete = [i for i in task_ids if "task_" + str(i) not in self.request.POST]
        SetTask.objects.filter(task_id__in=to_delete).delete()
        return "/admin/set?set_id=" + str(self.set.id)

    def post_time(self):
        try:
            tz = pytz.timezone("Europe/Moscow")
            if "start_time_check" in self.request.POST:
                self.set.start_time = None
            else:
                self.set.start_time = tz.localize(
                    datetime.datetime.strptime(
                        self.request.POST["start_time"], "%Y-%m-%dT%H:%M"
                    )
                )
            if "end_time_check" in self.request.POST:
                self.set.end_time = None
            else:
                self.set.end_time = tz.localize(
                    datetime.datetime.strptime(
                        self.request.POST["end_time"], "%Y-%m-%dT%H:%M"
                    )
                )
            self.set.opened = 'opened' in self.request.POST.keys()
            self.set.public = 'public' in self.request.POST.keys()
        except ValueError:
            return "/admin/set?set_id=" + str(self.set.id)
        self.set.save()
        return "/admin/set?set_id=" + str(self.set.id)

    def post_users_edit(self):
        current_users = self.set.editors
        for key, value in self.request.POST.items():
            if key.startswith("user_"):
                i = '_'.join(key.split("_")[1:])
                if i not in current_users:
                    self.set.editors.append(i)
        to_delete = [i for i in current_users if "user_" + i not in self.request.POST and i != self.request.user.username]
        for t in to_delete:
            self.set.editors.remove(t)
        self.set.save()
        return "/admin/set?set_id=" + str(self.set.id)

    def post_languages_edit(self):
        current_languages = self.set.languages
        self.set.auto_add_new_languages = 'auto_add' in self.request.POST
        for key, value in self.request.POST.items():
            if key.startswith("language_"):
                i = int(key.split("_")[1])
                if i not in current_languages:
                    self.set.languages.append(i)
        to_delete = [i for i in current_languages if "language_" + str(i) not in self.request.POST]
        for t in to_delete:
            self.set.languages.remove(t)
        self.set.save()
        return "/admin/set?set_id=" + str(self.set.id)

    def post_new_checker(self):
        Checker.objects.create(name=self.request.POST['name'], set=self.set, last_request=timezone.now() - datetime.timedelta(days=1))
        return '/admin/set?set_id=' + str(self.set.id)

    def post_delete_checker(self):
        Checker.objects.get(id=self.request.POST['checker_id']).delete()
        return '/admin/set?set_id=' + str(self.set.id)
