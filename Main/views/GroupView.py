from django.contrib.auth.models import User

from Main.models import Group
from SprintLib.BaseView import BaseView, AccessError
from SprintLib.utils import generate_token


class GroupView(BaseView):
    required_login = True
    endpoint = 'group'
    view_file = 'group.html'
    owner = False
    group: Group

    def pre_handle(self):
        self.owner = self.group.creator == self.request.user or self.request.user.username in self.group.editors

    def get(self):
        if self.owner:
            self.context['possible_users'] = set(self.group.users.all()) | set(self.request.user.userinfo.verified_friends)

    def post_sets_edit(self):
        if not self.owner:
            raise AccessError()
        current_sets = self.group.sets.all()
        set_ids = [set.id for set in current_sets]
        for key, value in self.request.POST.items():
            if key.startswith("set_"):
                i = int(key.split("_")[1])
                if i not in set_ids:
                    self.group.sets.add(i)
        to_delete = [i for i in set_ids if "set_" + str(i) not in self.request.POST]
        for t in to_delete:
            self.group.sets.remove(t)
        return "/group?group_id=" + str(self.group.id)

    def post_users_edit(self):
        if not self.owner:
            raise AccessError()
        current_users = self.group.users.all()
        users_ids = [user.id for user in current_users]
        for key, value in self.request.POST.items():
            if key.startswith("user_"):
                i = int(key.split("_")[1])
                if i not in users_ids:
                    self.group.users.add(i)
        to_delete = [i for i in users_ids if "user_" + str(i) not in self.request.POST]
        for t in to_delete:
            self.group.users.remove(t)
        return "/group?group_id=" + str(self.group.id)

    def link_action(self, value):
        if not self.owner:
            raise AccessError()
        self.group.access_token = value
        self.group.save()
        return "/group?group_id=" + str(self.group.id)

    def post_open_link(self):
        return self.link_action(generate_token())

    def post_close_link(self):
        return self.link_action(None)
