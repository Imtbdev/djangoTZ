from django import forms
from django.utils import timezone
from .models import UserProfile, WorkAssignment, Request


class WorkAssignmentForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(role='ispolnitel'),
        label='Ответственный:'
    )
    completion_date = forms.DateField(
        widget=forms.SelectDateWidget,
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
    class Meta:
        model = Request
        fields = ['equipment', 'issue_type', 'description', 'status']


class UserRequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['equipment', 'issue_type', 'description']
