from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from os.path import sep, join, exists
from os import remove

from Main.commands import shell
from Sprint.settings import MEDIA_ROOT
from django.core.exceptions import ObjectDoesNotExist
from json import loads


class Course(models.Model):
    name = models.TextField()

    @property
    def teachers(self):
        return [UserInfo.objects.get(user=s.user) for s in Subscribe.objects.filter(user__is_staff=1, course=self)]

    @property
    def subscribes(self):
        return sorted(Subscribe.objects.filter(course=self), key=lambda s: s.user.email)

    @property
    def students(self):
        userinfo = lambda sub: sub.user.userinfo
        return sorted(Subscribe.objects.filter(course=self, is_assistant=False, user__is_staff=False), key=lambda s: userinfo(s).surname + userinfo(s).name + userinfo(s).middle_name)

    def __str__(self):
        return self.name


class Block(models.Model):
    name = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    opened = models.BooleanField(default=False)
    show_rating = models.BooleanField(default=True)
    priority = models.IntegerField(default=5)
    cheating_checking = models.BooleanField(default=False)
    
    @property
    def messages(self):
        return Message.objects.filter(task__block=self)

    def __str__(self):
        return self.name

    @property
    def tasks(self):
        return Task.objects.filter(block=self)

    @property
    def time_start_chrome(self):
        return self.time_start.strftime("%Y-%m-%dT%H:%M")

    @property
    def time_end_chrome(self):
        return self.time_end.strftime("%Y-%m-%dT%H:%M")

    @property
    def is_opened(self):
        return 'checked' if self.opened else ''

    @property
    def solutions(self):
        return reversed(Solution.objects.filter(task__block=self))

    @property
    def subscribed_users(self):
        return [UserInfo.objects.get(user=s.user) for s in Subscribe.objects.filter(course=self.course)]

    @property
    def cheating_results_path(self):
        return join(MEDIA_ROOT, 'cheating_results', str(self.id))

    @property
    def cheating_checked(self):
        return self.cheating_results != {}

    @property
    def cheating_results(self):
        return loads(open(self.cheating_results_path, 'r').read()) if exists(self.cheating_results_path) else {}

    @property
    def cheating_status(self):
        if self.cheating_checking:
            return 'Идет проверка'
        if not exists(self.cheating_results_path):
            return 'Еще не проверено'
        return 'Проверка завершена'


class Restore(models.Model):
    code = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_assistant = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + '|' + self.course.name

    @property
    def userinfo(self):
        return UserInfo.objects.get(user=self.user)

    @property
    def role(self):
        if self.user.is_superuser:
            return 'Администратор'
        if self.user.is_staff:
            return 'Преподаватель'
        return 'Ассистент' if self.is_assistant else 'Студент'


class Task(models.Model):
    name = models.TextField()
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    legend = models.TextField(default='')
    input = models.TextField(default='')
    output = models.TextField(default='')
    specifications = models.TextField(default='')
    time_limit = models.IntegerField(default=10000)
    weight = models.FloatField(default=1.0)
    max_mark = models.IntegerField(default=10)
    max_solutions_count = models.IntegerField(default=10)
    show_result = models.BooleanField(default=True)
    show_details = models.BooleanField(default=False)
    full_solution = models.BooleanField(default=False)
    mark_formula = models.TextField(default='None')
    priority = models.IntegerField(default=5)

    @property
    def students_solutions(self):
        students = [sub.user for sub in Subscribe.objects.filter(course=self.block.course)]
        solutions = Solution.objects.filter(task=self)
        return [sol for sol in solutions if sol.user in students]

    @property
    def correct_count(self):
        solutions = self.students_solutions
        count = 0
        for sol in solutions:
            res = sol.result.split('/')
            if len(res) == 2 and res[0] == res[1]:
                count += 1
        return count

    @property
    def solutions_count(self):
        return len(self.students_solutions)

    @property
    def partially_passed(self):
        solutions = self.students_solutions
        count = 0
        for sol in solutions:
            res = sol.result.split('/')
            if len(res) == 2 and res[0] != res[1]:
                count += 1
        return count

    @property
    def solutions_with_error(self):
        return self.solutions_count - self.correct_count - self.partially_passed

    @property
    def samples(self):
        return [{
                'input': file,
                'output': file.answer
            } for file in ExtraFile.objects.filter(task=self, sample=True).order_by('filename')]

    def __hash__(self):
        return self.id

    @property
    def showable(self):
        return 'checked' if self.show_details else ''
    

    def __str__(self):
        return self.name

    def tests_path(self):
        return join(MEDIA_ROOT, 'tests', str(self.id) + '.cs')

    @property
    def tests_text(self):
        try:
            return open(self.tests_path(), 'r').read()
        except FileNotFoundError:
            with open(self.tests_path(), 'w') as fs:
                pass
            return ''

    @property
    def tests_uploaded(self):
        from os.path import exists
        return exists(self.tests_path())

    @property
    def files(self):
        return ExtraFile.objects.filter(task=self).order_by('filename')

    @property
    def files_for_compilation(self):
        return ExtraFile.objects.filter(task=self, for_compilation=True)
    

    @property
    def is_full_solution(self):
        return 'checked' if self.full_solution else ''
    

class UserInfo(models.Model):
    surname = models.TextField()
    name = models.TextField()
    middle_name = models.TextField()
    group = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __eq__(self, obj):
        return str(self) == str(obj)

    def __hash__(self):
        return self.id

    def __str__(self):
        return "{} {} {}".format(self.surname, self.name, self.middle_name)


class Solution(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.TextField()
    details = models.TextField(default='')
    time_sent = models.DateTimeField(null=True)
    mark = models.IntegerField(null=True)
    comment = models.TextField(default='')

    def set_result(self, result):
        self.result = result
        if len(result.split('/')) != 1:
            result = int(result.split('/')[0])
        try:
            self.mark = eval(self.task.mark_formula)
        except:
            self.mark = None
        self.save()

    def __str__(self):
        return str(self.id)

    def path(self):
        return join(MEDIA_ROOT, 'solutions', str(self.id))

    def write_log(self, text):
        with self.log_fs as fs:
            fs.write(bytes(text + '\n', 'cp866'))

    @property
    def log_file(self):
        return join(MEDIA_ROOT, 'logs', str(self.id) + '.log')

    @property
    def log_text(self):
        try:
            return open(self.log_file, 'rb').read().decode('cp866')
        except FileNotFoundError:
            return ''

    @property
    def log_fs(self):
        return open(self.log_file, 'ab')

    @property
    def userinfo(self):
        return UserInfo.objects.get(user=self.user)

    @property
    def mark_property(self):
        return str(self.mark) if self.mark is not None else 'нет оценки'

    @property
    def mark_select(self):
        line = ''
        if self.mark:
            line += '<option value="нет оценки">нет оценки</option>'
        else:
            line += '<option value="нет оценки" selected>нет оценки</option>'
        for mark in range(self.task.max_mark + 1):
            if mark == self.mark:
                line += '<option value="{}" selected>{}</option>'.format(mark, mark)
            else:
                line += '<option value="{}">{}</option>'.format(mark, mark)
        return line

    @property
    def comment_property(self):
        return self.comment if self.comment else 'нет комментария'

    @staticmethod
    def get_files(path):
        from os import listdir
        from os.path import isfile, join
        files_dict = {}
        for file in listdir(path):
            if file == '__MACOSX' or file == 'test_folder' or file == 'bin' or file == 'obj' or file == '.vs':
                continue
            current_file = join(path, file)
            if isfile(current_file):
                if not current_file.endswith('.csproj') and not current_file.endswith('.sln'):
                    try:
                        files_dict[sep.join(current_file.split('solutions' + sep)[1].split(sep)[1:])] \
                            = open(current_file, 'rb').read().decode('UTF-8')
                    except UnicodeDecodeError:
                        pass
            else:
                files_dict = {**files_dict, **Solution.get_files(current_file)}
        return files_dict

    @property
    def files(self):
        return Solution.get_files(self.path())

    @property
    def user_files(self):
        f = {}
        comp_files = [ef.filename for ef in ExtraFile.objects.filter(task=self.task, for_compilation=True)]
        for fi in self.files.keys():
            if not fi in comp_files:
                f[fi] = self.files[fi]
        return f

    @property
    def passed_all_tests(self):
        spl = self.result.split('/')
        return len(spl) == 2 and spl[0] == spl[1]

class System(models.Model):
    key = models.TextField()
    value = models.TextField()

    def __str__(self):
        return self.key


class ExtraFile(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    filename = models.TextField()
    for_compilation = models.BooleanField(default=False)
    sample = models.BooleanField(default=False)

    @property
    def answer(self):
        try:
            return ExtraFile.objects.get(task=self.task, filename=self.filename + '.a')
        except ObjectDoesNotExist:
            return None

    @property
    def num(self):
        try:
            return int(self.filename.split('.')[0])
        except ValueError:
            return ''

    @property
    def is_for_compilation(self):
        return 'checked' if self.for_compilation else ''

    @property
    def is_sample(self):
        return 'checked' if self.sample else ''
    
    @property
    def can_be_sample(self):
        try:
            int(self.filename)
        except:
            return False
        try:
            ans = ExtraFile.objects.get(task=self.task, filename=self.filename + '.a')
        except ObjectDoesNotExist:
            return False
        return self.readable and ans.readable
    

    @property
    def path(self):
        return join(MEDIA_ROOT, 'extra_files', str(self.id))
    

    @property
    def readable(self):
        try:
            open(self.path, 'rb').read().decode('UTF-8')
            return True
        except UnicodeDecodeError:
            return False

    @property
    def text(self):
        return open(self.path, 'rb').read().decode('UTF-8')
    

    def __str__(self):
        return self.filename


    def write(self, data):
        with open(self.path, 'wb') as fs:
            fs.write(data)


class Message(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reply_to = models.ForeignKey('Message', on_delete=models.CASCADE, null=True)
    for_all = models.BooleanField()
    text = models.TextField()


@receiver(post_delete, sender=Task)
def delete_task_hook(sender, instance, using, **kwargs):
    if exists(instance.tests_path()):
        from os import remove
        remove(instance.tests_path())


@receiver(post_delete, sender=Solution)
def delete_solution_hook(sender, instance, using, **kwargs):
    if exists(instance.path()):
        from shutil import rmtree
        rmtree(instance.path())
    shell('docker rm --force solution_container_{}'.format(instance.id))
    shell('docker image rm solution_{}'.format(instance.id))


@receiver(post_delete, sender=ExtraFile)
def delete_file_hook(sender, instance, using, **kwargs):
    try:
        if exists(instance.path):
            remove(instance.path)
    except ValueError:
        pass
    if instance.filename.endswith('.a'):
        try:
            t = ExtraFile.objects.get(task=instance.task, filename=instance.filename[:-2])
        except ObjectDoesNotExist:
            return
        t.sample = False
        t.save()
