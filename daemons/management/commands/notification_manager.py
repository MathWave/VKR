from django.contrib.auth.models import User

from Main.models import Solution, Progress
from SprintLib.queue import MessagingSupport, send_to_queue


class Command(MessagingSupport):
    help = "starts file notification manager"
    queue_name = "notification"

    def handle_solution(self, payload):
        solution = Solution.objects.get(id=payload["solution_id"])
        user = solution.user
        if user.userinfo.notification_solution_result:
            message = f"Задача: {solution.task.name}\n" \
                      f"Результат: {solution.result}\n" \
                      f"Очки решения: {Progress.by_solution(solution).score}\n" \
                      f"Текущий рейтинг: {solution.user.userinfo.rating}"
            if user.userinfo.notification_telegram is not None:
                yield "telegram", {"chat_id": user.userinfo.telegram_chat_id, "text": message}
            if user.userinfo.notification_email:
                yield "email", {"subject": "Тестирование завершено", "message": message, "email": user.email}

    def handle_friends_add(self, payload):
        user = User.objects.get(id=payload['to_user'])
        from_user = User.objects.get(id=payload['from_user'])
        if user.userinfo.notification_friends:
            message = f"Пользователь {from_user.username} хочет добавить тебя в друзья"
            if user.userinfo.notification_telegram:
                yield "telegram", {"chat_id": user.userinfo.telegram_chat_id, "text": message}
            if user.userinfo.notification_email:
                yield "email", {"subject": "Новая заявка в друзья", "message": message, "email": user.email}

    def handle_friends_accept(self, payload):
        user = User.objects.get(id=payload['to_user_id'])
        from_user = User.objects.get(id=payload['from_user_id'])
        if user.userinfo.notification_friends:
            if payload['accepted']:
                message = f"Пользователь {from_user} одобрил заявку в друзья"
            else:
                message = f"Пользователь {from_user} отклонил заявку в друзья"
            if user.userinfo.notification_telegram:
                yield "telegram", {"chat_id": user.userinfo.telegram_chat_id, "text": message}
            if user.userinfo.notification_email:
                yield "email", {"subject": "Новая заявка в друзья", "message": message, "email": user.email}

    def process(self, payload: dict):
        notification_type = payload["type"]
        handler = getattr(self, "handle_" + notification_type, None)
        if handler is None:
            raise ValueError(f"Unknown type: {notification_type}")
        for queue, payload in handler(payload):
            send_to_queue(queue, payload)
