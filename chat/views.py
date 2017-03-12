from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

from itertools import chain

from .models import Thread, Message


def _get_or_create_thread(user1, user2):
    if user1.id < user2.id:
        users = {'user1': user1, 'user2': user2}
    else:
        users = {'user1': user2, 'user2': user1}

    try:
        thread = Thread.objects.get(**users)
    except Thread.DoesNotExist:
        thread = Thread.objects.create(**users)

    return thread


def index(request):
    querysets = [Thread.objects.filter(user1=request.user), Thread.objects.filter(user2=request.user)]
    threads = list(chain(*querysets))

    context = {
        'threads': threads,
    }

    return render(request, "chat/index.html", context)


def thread(request, pk):
    querysets = [Thread.objects.filter(user1=request.user), Thread.objects.filter(user2=request.user)]
    threads = list(chain(*querysets))

    # thread = _get_or_create_thread(request.user, User.objects.get(username=username))
    thread = Thread.objects.get(id=pk)
    messages = Message.objects.filter(thread=thread)

    context = {
        'threads': threads,
        'messages': messages,
    }

    return render(request, "chat/index.html", context)


def send_message(request, pk):
    if request.method == "POST":

        author = request.user

        thread = Thread.objects.get(id=pk)

        if thread.user1 == author:
            receiver = thread.user2
        else:
            receiver = thread.user1

        text = request.POST.get('msg')

        # thread = _get_or_create_thread(author, receiver)

        try:
            Message.objects.create(thread=thread, author=author, text=text, receiver=receiver)
        except:
            return JsonResponse({'status': 'Message object not created', 'text': text})
        else:
            return JsonResponse({'status': 'Message sent', 'text': text})
            # return HttpResponseRedirect(reverse('chat:index'))
    else:
        return JsonResponse({'status': 'Message not sent'})
