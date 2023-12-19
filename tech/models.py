from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    USER_ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('ispolnitel', 'Исполнитель'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='user', verbose_name='Роль')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)


class Notification(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Профиль пользователя')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Уведомление для {self.user_profile.user.username}'

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'


class Equipment(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'


class IssueType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип проблемы'
        verbose_name_plural = 'Типы проблем'


class Comment(models.Model):
    request = models.ForeignKey('Request', on_delete=models.CASCADE, related_name='comments', verbose_name='Заявка')
    author = models.ForeignKey(UserProfile, limit_choices_to={'role': 'ispolnitel'}, on_delete=models.CASCADE,
                               verbose_name='Автор')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Комментарий от {self.author.user.username} к заявке #{self.request.number}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Request(models.Model):
    number = models.AutoField(primary_key=True, verbose_name='Номер заявки')
    date_added = models.DateField(auto_now_add=True, verbose_name='Дата добавления')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование')
    issue_type = models.ForeignKey(IssueType, on_delete=models.CASCADE, verbose_name='Тип проблемы')
    description = models.TextField(verbose_name='Описание')
    client = models.ForeignKey(UserProfile, limit_choices_to={'role': 'user', 'user__is_staff': False},
                               on_delete=models.CASCADE, verbose_name='Клиент')
    status_choices = [
        ('pending', 'В ожидании'),
        ('in_progress', 'В работе'),
        ('completed', 'Выполнена'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending', verbose_name='Статус')
    date_closed = models.DateField(null=True, blank=True, verbose_name='Дата закрытия')

    def __str__(self):
        return str(self.number)

    def get_absolute_url(self):
        return reverse('request_detail', args=[str(self.pk)])

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.date_closed:
            self.date_closed = timezone.now().date()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class WorkAssignment(models.Model):
    request = models.OneToOneField(Request, on_delete=models.CASCADE, verbose_name='Заявка')
    assigned_to = models.ForeignKey(UserProfile, limit_choices_to={'role': 'ispolnitel'}, on_delete=models.CASCADE,
                                    verbose_name='Исполнитель')
    completion_date = models.DateField(null=True, blank=True, verbose_name='Дата завершения')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Работа по заявке'
        verbose_name_plural = 'Работы по заявкам'


@receiver(post_save, sender=Request)
def request_status_changed(sender, instance, **kwargs):
    if instance.status == 'completed':
        notification_message = f'Заявка #{instance.number} выполнена.'
    else:
        notification_message = f'Заявка #{instance.number} {instance.get_status_display()}.'

    Notification.objects.create(user_profile=instance.client, message=notification_message)

    class Meta:
        verbose_name = 'Изменение статуса заявки'
        verbose_name_plural = 'Изменения статусов заявок'
