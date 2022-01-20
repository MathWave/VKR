from django.db.models import Q

from Main.models import SetTask, Task
from SprintLib.BaseView import BaseView


class SetSettingsView(BaseView):
    required_login = True
    view_file = "set_settings.html"
    endpoint = "admin/set"

    def get(self):
        self.context['settasks'] = SetTask.objects.filter(set=self.entities.set).order_by('name')
        self.context['tasks'] = Task.objects.filter(Q(public=True) | Q(creator=self.request.user) | Q(editors__in=self.request.user.username)).order_by('name')

    def post_save(self):
        for key, value in self.request.POST.items():
            if key.startswith('settask_'):
                st = SetTask.objects.get(id=key.split('_')[1])
                st.name = value
                st.save()
        self.entities.set.name = self.request.POST['name']
        self.entities.set.save()
        return '/admin/set?set_id=' + str(self.entities.set.id)

    def post_edit(self):
        current_tasks = self.entities.set.tasks
        task_ids = [task.id for task in current_tasks]
        for key, value in self.request.POST.items():
            if key.startswith('task_'):
                i = int(key.split('_')[1])
                if i not in task_ids:
                    SetTask.objects.create(set=self.entities.set, task_id=i)
        to_delete = [i for i in task_ids if 'task_' + str(i) not in self.request.POST]
        SetTask.objects.filter(task_id__in=to_delete).delete()
        return '/admin/set?set_id=' + str(self.entities.set.id)
