from django.contrib.auth.models import User

from SprintLib.BaseView import BaseView
from SprintLib.utils import delete_file, write_bytes


class AccountView(BaseView):
    view_file = "account.html"
    required_login = True
    endpoint = "account"

    def get(self):
        if "username" in self.request.GET.keys():
            self.context["account"] = User.objects.get(
                username=self.request.GET["username"]
            )
        else:
            self.context["account"] = self.request.user
        self.context["owner"] = self.context["account"] == self.request.user
        self.context["error_message"] = self.request.GET.get("error_message", "")

    def post_upload_photo(self):
        if self.request.user.userinfo.has_profile_pic:
            delete_file(self.request.user.userinfo.profile_picture_fs_id)
        fs_id = write_bytes(self.request.FILES["file"].read())
        self.request.user.userinfo.profile_picture_fs_id = fs_id
        self.request.user.userinfo.save()
        return "/account"

    def post_set_language(self):
        lang_id = int(self.request.POST["language"])
        self.request.user.userinfo.favourite_language_id = lang_id if lang_id != -1 else None
        self.request.user.userinfo.save()
        return "/account"

    def post_notifications(self):
        for attr in dir(self.request.user.userinfo):
            if attr.startswith('notification'):
                setattr(self.request.user.userinfo, attr, attr in self.request.POST.keys())
        self.request.user.userinfo.save()
        return '/account'
