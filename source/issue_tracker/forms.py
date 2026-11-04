
from django import forms
from django.forms import widgets

from issue_tracker.models import Task, Status, Type

class TaskForm(forms.ModelForm):
    status = forms.ModelChoiceField(queryset=Status.objects.all())
    type = forms.ModelChoiceField(queryset=Type.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Task
        fields = ('summary', 'description', 'status', 'type')
        widgets = {
            'description': widgets.Textarea(attrs={'cols': '40', 'rows': '5'}),
        }
