from __future__ import unicode_literals

from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Timestamped(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Thread(Timestamped):
    user1 = models.ForeignKey(User, related_name='user1_thread')
    user2 = models.ForeignKey(User, related_name='user2_thread')

    def __str__(self):
        return "{user1} - {user2}".format(user1=self.user1, user2=self.user2)

    class Meta:
        ordering = ['updated']


class Message(Timestamped):
    thread = models.ForeignKey(Thread)
    author = models.ForeignKey(User, related_name='sent_message')
    text = models.TextField()
    receiver = models.ForeignKey(User, related_name='received_message')

    def __str__(self):
        return "{author} -> {receiver} : {text}".format(author=self.author, receiver=self.receiver, text=self.text)
