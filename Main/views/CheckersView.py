import datetime
from typing import Optional

import pytz
from django.utils import timezone

from Checker.models import Checker
from Main.models import SetTask, Set
from SprintLib.BaseView import BaseView, AccessError
from SprintLib.language import languages


class CheckersView(BaseView):
    required_login = True
    view_file = "checkers.html"
    endpoint = "admin/checkers"

    def pre_handle(self):
        self.current_set = self.entities.set
        if (
            self.request.user != self.current_set.creator
            and self.request.user.username not in self.current_set.editors
        ):
            raise AccessError()
