from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model
import uuid

# Create your models here.


class Ticket(models.Model):

    TICKET_SECTIONS = (
        ('Software', 'Software'),
        ('Hardware', 'Hardware'),
        ('Applications', 'Applications'),
        ('Infrastructure and Networking', 'Infrastructure and Networking'),
        ('Database Administrator', 'Database Administrator')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    customer_full_name = models.CharField(max_length=200)
    customer_phone_number = models.CharField(max_length=20)
    customer_email = models.EmailField(max_length=40)
    issue_description = models.TextField(max_length=1000)
    ticket_section = models.CharField(
        max_length=30, choices=TICKET_SECTIONS, null=True, blank=True)
    urgent_status = models.BooleanField(default=False)
    completed_status = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='assigned_to', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("ticketapp:ticket-detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    created_date = models.DateTimeField(null=True, auto_now_add=True)
