from SprintLib.BaseView import BaseView


class SetView(BaseView):
    required_login = True
    endpoint = 'set'
    view_file = 'set.html'
