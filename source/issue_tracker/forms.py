
from django import forms
from django.forms import widgets


from issue_tracker.models import Task, Status, Type
from issue_tracker.validators import BanWordValidator, IsItLinkValidator, MinLengthValidator

class TaskForm(forms.ModelForm):
    status = forms.ModelChoiceField(queryset=Status.objects.all())


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Task
        fields = ('summary', 'description', 'status', 'types')
        widgets = {
            'description': widgets.Textarea(attrs={'cols': '40', 'rows': '5'}
        ),
            'types': widgets.CheckboxSelectMultiple(),
        }
        validators = {
            'summary': [IsItLinkValidator(), BanWordValidator(), MinLengthValidator(8)],
            'description': [IsItLinkValidator(), BanWordValidator(), MinLengthValidator(10)],
        }
