from django.shortcuts import render

from Messaging.models import Chat, Message, Membership
from SprintLib.BaseView import AccessError

page_size = 20


def chat_window(request):
    chat = None if request.GET['chat_id'] == '-1' else Chat.objects.get(id=request.GET['chat_id'])
    if chat is not None:
        if Membership.objects.filter(user=request.user, chat=chat).first() is None:
            raise AccessError()
    page = None if request.GET['page'] == '-1' else int(request.GET['page'])
    memberships = Membership.objects.filter(user=request.user).order_by('-chat__last_message__time_sent')
    messages = []
    if chat is not None:
        offset = page_size * (page - 1)
        limit = page_size
        Message.objects.filter(chat=chat, is_read=False).update(is_read=True)
        messages = Message.objects.filter(chat=chat).order_by('-time_sent')[offset:offset + limit]
    return render(request, "chat_window.html", context={
        "memberships": memberships,
        "messages": messages,
        "current_chat": chat,
    })
