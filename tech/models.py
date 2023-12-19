from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USER_ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('ispolnitel', 'Исполнитель'),
        ('admin', 'Администратор'),
    ]

    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='user')

    def __str__(self):
        return self.user.username


class Equipment(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class IssueType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Comment(models.Model):
    request = models.ForeignKey('Request', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(UserProfile, limit_choices_to={'role': 'ispolnitel'}, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.user.username} on Request #{self.request.number}'


class Request(models.Model):
    number = models.AutoField(primary_key=True)
    date_added = models.DateField(auto_now_add=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    issue_type = models.ForeignKey(IssueType, on_delete=models.CASCADE)
    description = models.TextField()
    client = models.ForeignKey(UserProfile, limit_choices_to={'role': 'user', 'user__is_staff': False},
                               on_delete=models.CASCADE)
    status_choices = [
        ('pending', 'В ожидании'),
        ('in_progress', 'В работе'),
        ('completed', 'Выполнено'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    date_closed = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.number)

    def get_absolute_url(self):
        return reverse('request_detail', args=[str(self.pk)])

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.date_closed:
            self.date_closed = timezone.now().date()
        super().save(*args, **kwargs)


class WorkAssignment(models.Model):
    request = models.OneToOneField(Request, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(UserProfile, limit_choices_to={'role': 'ispolnitel'}, on_delete=models.CASCADE)
    completion_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.pk)
