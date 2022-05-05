from os.path import join
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse

from django.utils import timezone

from Checker.models import Checker
from FileStorage.sync import synchronized_method
from Main.models import Solution, SolutionFile, ExtraFile, Progress
from SprintLib.utils import generate_token
from SprintLib.queue import notify as notification


def get_dynamic(request):
    try:
        checker = Checker.objects.get(token=request.GET['token'])
        if checker.status == 'Active':
            return JsonResponse({"status": "Another checker is working"}, status=403)
        checker.dynamic_token = generate_token()
        checker.save()
        return JsonResponse({"token": checker.dynamic_token})
    except ObjectDoesNotExist:
        return JsonResponse({"status": "incorrect token"}, status=403)


def status(request):
    try:
        checker = Checker.objects.get(dynamic_token=request.GET['token'])
        now = timezone.now()
        checker.last_request = now
        checker.save()
        return JsonResponse({"status": "ok"})
    except ObjectDoesNotExist:
        return JsonResponse({"status": "incorrect token"}, status=403)


@synchronized_method
def available(request):
    try:
        checker = Checker.objects.get(dynamic_token=request.GET['token'])
        solution = Solution.objects.filter(set=checker.set, result="In queue").order_by('time_sent').first()
        if solution is None:
            return JsonResponse({"id": None})
        solution.result = "Testing"
        solution.save()
        checker.testing_solution = solution
        checker.save()
        with TemporaryDirectory() as tempdir:
            with ZipFile(join(tempdir, "package.zip"), 'w') as zip_file:
                for sf in SolutionFile.objects.filter(solution=solution):
                    zip_file.writestr(join('solution', sf.path), sf.bytes)
                for ef in ExtraFile.objects.filter(task=solution.task):
                    zip_file.writestr(ef.filename, ef.bytes)
            response = HttpResponse(open(join(tempdir, 'package.zip'), 'rb').read(), content_type='application/octet-stream', status=201)
            response.headers['language_id'] = solution.language_id
            response.headers['solution_id'] = solution.id
            response.headers['timeout'] = solution.task.time_limit
            return response
    except ObjectDoesNotExist:
        return JsonResponse({"status": "incorrect token"}, status=403)


def save_solution(request):
    try:
        checker = Checker.objects.get(dynamic_token=request.GET['token'])
        solution = Solution.objects.get(id=request.GET['solution_id'])
        result = request.GET['result']
        test = request.GET.get("test")
        extras = request.GET.get('extras')
        if checker.set != solution.set:
            return JsonResponse({"status": "incorrect solution"}, status=403)
        solution.result = result
        solution.test = test
        solution.extras = extras
        if result == 'OK':
            solution.test = None
        solution.save()
        if not result.startswith('Testing'):
            checker.testing_solution = None
            checker.save()
        return JsonResponse({"status": True})
    except ObjectDoesNotExist:
        return JsonResponse({"status": "incorrect token"}, status=403)


def notify(request):
    try:
        checker = Checker.objects.get(dynamic_token=request.GET['token'])
        solution = Solution.objects.get(id=request.GET['solution_id'])
        if checker.set != solution.set:
            return JsonResponse({"status": "incorrect solution"}, status=403)
        notification(
            solution.user,
            "solution_result",
            f"Задача: {solution.task.name}\n"
            f"Результат: {solution.result}\n"
            f"Очки решения: {Progress.by_solution(solution).score}\n"
            f"Текущий рейтинг: {solution.user.userinfo.rating}")
        return JsonResponse({"status": True})
    except ObjectDoesNotExist:
        return JsonResponse({"status": "incorrect token"}, status=403)


def save_progress(request):
    try:
        checker = Checker.objects.get(dynamic_token=request.GET['token'])
        solution = Solution.objects.get(id=request.GET['solution_id'])
        if checker.set != solution.set:
            return JsonResponse({"status": "incorrect solution"}, status=403)
        progress = Progress.objects.get(
            user=solution.user, task=solution.task
        )
        if progress.finished_time is None:
            progress.finished_time = solution.time_sent
            progress.finished = True
            progress.save()
            progress.increment_rating()
        return JsonResponse({"status": True})
    except ObjectDoesNotExist:
        return JsonResponse({"status": "incorrect token"}, status=403)
