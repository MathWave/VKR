from Main.models import Set
from SprintLib.BaseView import BaseView


class SetsView(BaseView):
    view_file = "sets.html"
    required_login = True
    endpoint = "sets"

    def post(self):
        set_name = self.request.POST["name"]
        set = Set.objects.create(name=set_name, creator=self.request.user)
        return f"/admin/set?set_id={set.id}"
