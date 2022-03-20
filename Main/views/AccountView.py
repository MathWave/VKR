from django.contrib.auth.models import User
from django.db.models import Q

from SprintLib.queue import notify
from Main.models import Friendship
from SprintLib.BaseView import BaseView
from SprintLib.language import languages
from SprintLib.utils import delete_file, write_bytes


class AccountView(BaseView):
    view_file = "account.html"
    required_login = True
    endpoint = "account"

    def pre_handle(self):
        if "username" in self.request.GET.keys():
            self.context["account"] = User.objects.get(
                username=self.request.GET["username"]
            )
        else:
            self.context["account"] = self.request.user
        self.context["owner"] = self.context["account"] == self.request.user

    def get(self):
        self.context["error_message"] = self.request.GET.get("error_message", "")
        self.context['languages'] = languages
        friendship = Friendship.objects.filter(
            Q(from_user=self.request.user, to_user=self.context["account"])
            | Q(to_user=self.request.user, from_user=self.context["account"])
        ).first()
        if friendship is None:
            self.context["friendship_status"] = 0
        elif friendship.verified:
            self.context["friendship_status"] = 1
        elif friendship.from_user == self.request.user:
            self.context["friendship_status"] = 2
        else:
            self.context["friendship_status"] = 3

    def post_friendship(self):
        if "to_do" in self.request.POST:
            friendship = Friendship.objects.filter(
                Q(from_user=self.request.user, to_user=self.context["account"])
                | Q(to_user=self.request.user, from_user=self.context["account"])
            ).first()
            if friendship is None:
                Friendship.objects.create(from_user=self.request.user, to_user=self.context["account"])
                notify(self.context['account'], 'friends', f"Пользователь {self.request.user.username} хочет добавить тебя в друзья")
            elif friendship.verified or friendship.from_user == self.request.user:
                friendship.delete()
            else:
                if self.request.POST["to_do"] == "yes":
                    friendship.verified = True
                    friendship.save()
                    notify(self.context['account'], 'friends', f"Пользователь {self.request.user.username} добавил тебя в друзья")
                else:
                    friendship.delete()
                    notify(self.context['account'], 'friends', f"Пользователь {self.request.user.username} отклонил твою заявку")
        return "/account?username=" + self.request.GET["username"]

    def post_upload_photo(self):
        if self.request.user.userinfo.has_profile_pic:
            delete_file(self.request.user.userinfo.profile_picture_fs_id)
        fs_id = write_bytes(self.request.FILES["file"].read())
        self.request.user.userinfo.profile_picture_fs_id = fs_id
        self.request.user.userinfo.save()
        return "/account"

    def post_set_language(self):
        lang_id = int(self.request.POST["language"])
        self.request.user.userinfo.favourite_language_id = (
            lang_id if lang_id != -1 else None
        )
        self.request.user.userinfo.save()
        return "/account"

    def post_notifications(self):
        for attr in dir(self.request.user.userinfo):
            if attr.startswith("notification"):
                setattr(
                    self.request.user.userinfo, attr, attr in self.request.POST.keys()
                )
        self.request.user.userinfo.save()
        return "/account"
