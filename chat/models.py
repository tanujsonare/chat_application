from django.db import models

from account.models import User


class Message(models.Model):
    sent_by = models.CharField(max_length=255, blank=True, null=True)
    receiver_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="receiver_user")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f'{self.sender_user.name}'


class Room(models.Model):
    WAITING = "waiting"
    ACTIVE = "active"
    CLOSED = "closed"

    CHOICES_STATUS = (
        (WAITING, "waiting"),
        (ACTIVE, "active"),
        (CLOSED, "closed"),
    )
    uuid = models.CharField(max_length=255)
    client = models.CharField(max_length=255)
    agent = models.ForeignKey(User, null=True, blank=True, related_name="rooms", on_delete=models.CASCADE)
    message = models.ManyToManyField(Message, blank=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=WAITING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f'{self.client} - {self.uuid}'