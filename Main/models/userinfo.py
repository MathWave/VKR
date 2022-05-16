from functools import cached_property

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils import timezone

from Main.models.group import Group
from Main.models.friendship import Friendship
from Main.models.set import Set
from Main.models.task import Task
from Sprint.settings import CONSTS
from SprintLib.language import languages


class UserInfo(models.Model):
    surname = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    last_request = models.DateTimeField(default=timezone.now)
    profile_picture_fs_id = models.IntegerField(null=True, blank=True)
    favourite_language_id = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    telegram_chat_id = models.TextField(default="", null=True, blank=True)
    vk_user_id = models.IntegerField(null=True, blank=True)
    notification_solution_result = models.BooleanField(default=False)
    notification_friends = models.BooleanField(default=False)
    notification_messages = models.BooleanField(default=False)
    notification_telegram = models.BooleanField(default=False)
    notification_email = models.BooleanField(default=False)
    code = models.IntegerField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.surname + ' ' + self.name

    @property
    def groups(self):
        return Group.objects.filter(Q(creator=self.user) | Q(editors__in=self.user.username))

    @property
    def tasks_solved(self):
        fltr = Task.objects.filter(solution__result=CONSTS["ok_status"], solution__user=self.user).distinct()
        return len(fltr)

    @property
    def has_favourite_language(self):
        return self.favourite_language_id is not None

    @property
    def verified_friends(self):
        return User.objects.filter(Q(to_friendship__from_user=self.user) | Q(from_friendship__to_user=self.user))

    @cached_property
    def friends(self):
        return Friendship.objects.filter(Q(to_user=self.user) | Q(from_user=self.user)).order_by("verified")

    @property
    def favourite_language(self):
        if not self.has_favourite_language:
            return None
        return languages[self.favourite_language_id]

    @cached_property
    def available_tasks(self):
        return Task.objects.filter(Q(public=True) | Q(creator=self.user) | Q(editors__contains=[self.user.username]))

    @property
    def available_sets(self):
        return Set.objects.filter(Q(public=True) | Q(creator=self.user) | Q(editors__contains=[self.user.username])).order_by('name')

    @property
    def place(self):
        return len(UserInfo.objects.filter(rating__gt=self.rating)) + 1

    @property
    def activity_status(self):
        if timezone.now() - self.last_request <= timezone.timedelta(minutes=5):
            return CONSTS["online_status"]
        return timezone.datetime.strftime(self.last_request, "%d-%m-%Y %H:%M")

    @property
    def can_create(self):
        return self.user.is_superuser or self.teacher

    @property
    def has_profile_pic(self):
        try:
            return self.profile_picture_fs_id is not None
        except ValueError:
            return False

    @property
    def profile_pic_url(self):
        if self.has_profile_pic:
            return "/image?id=" + str(self.profile_picture_fs_id)
        return "/static/img/user.png"
