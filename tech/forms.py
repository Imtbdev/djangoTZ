from django import forms
from django.forms import DateInput
from django.utils import timezone
from .models import UserProfile, WorkAssignment, Request, Equipment, IssueType


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
