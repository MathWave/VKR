from SprintLib.BaseView import BaseView


class SolutionsView(BaseView):
    required_login = True
    endpoint = "solutions"
    view_file = "solutions.html"
