from django import template

from Main.models import Solution, SetTask

register = template.Library()


@register.filter('solved')
def solved(user, task):
    solutions = Solution.objects.filter(user=user, task=task)
    if len(solutions.filter(result='OK')) != 0:
        return True
    if len(solutions) != 0:
        return False
    return None


@register.filter('settask')
def settask(set, task):
    return SetTask.objects.get(set=set, task=task)


@register.filter('startswith')
def startswith(s, prefix):
    return s is not None and s.startswith(prefix)


@register.filter('make_pair')
def make_pair(user, task):
    return user, task


@register.filter('get_info')
def get_info(data, pair):
    return data.get(pair)
