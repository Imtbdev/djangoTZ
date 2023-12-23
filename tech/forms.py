from django import forms
from django.contrib.auth.models import User
from django.forms import DateInput
from django.utils import timezone
from .models import WorkAssignment, Request, Equipment, IssueType, UserProfile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _


class WorkAssignmentForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(role='ispolnitel'),
        label='Ответственный:',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    completion_date = forms.DateField(
        widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Дата окончания работ:'
    )

    class Meta:
        model = WorkAssignment
        fields = ['assigned_to', 'completion_date', ]

    def clean_completion_date(self):
        completion_date = self.cleaned_data.get('completion_date')

        if completion_date and completion_date < timezone.now().date():
            raise forms.ValidationError('Дата окончания работ не может быть в прошлом.')

        return completion_date


class RequestForm(forms.ModelForm):
    equipment = forms.ModelChoiceField(
        queryset=Equipment.objects.all(),
        label='Оборудование:',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    issue_type = forms.ModelChoiceField(
        queryset=IssueType.objects.all(),
        label='Тип проблемы:',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Описание:'
    )
    status = forms.ChoiceField(
        choices=Request.status_choices,
        label='Статус:',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    client = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(role='user'),
        label='Клиент:',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Request
        fields = ['equipment', 'issue_type', 'description', 'status']


class UserRequestForm(forms.ModelForm):
    equipment = forms.ModelChoiceField(
        queryset=Equipment.objects.all(),
        label='Оборудование:',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    issue_type = forms.ModelChoiceField(
        queryset=IssueType.objects.all(),
        label='Тип проблемы:',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Описание:'
    )

    class Meta:
        model = Request
        fields = ['equipment', 'issue_type', 'description']


class StyledAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Имя пользователя',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль',
    )


class StyledUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Имя пользователя',
        help_text=_('Обязательное поле. Не более 30 символов.'),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль',
        help_text=_('Пароль не может состоять только из цифр и быть слишком простым.'),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Подтвердите пароль',
        help_text=_("Введите тот же пароль, что и выше, для подтверждения."),
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class DescriptionForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Описание:'
    )

    class Meta:
        model = Request
        fields = ['description']
