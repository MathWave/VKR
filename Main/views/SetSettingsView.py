from SprintLib.BaseView import BaseView


class SetSettingsView(BaseView):
    required_login = True
    view_file = "set_settings.html"
    endpoint = "admin/set"
