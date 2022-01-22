from django import template

from Main.models import Solution

register = template.Library()


@register.filter('solved')
def solved(user, task):
    solutions = Solution.objects.filter(user=user, task=task)
    if len(solutions.filter(result='OK')) != 0:
        return True
    if len(solutions) != 0:
        return False
    return None
