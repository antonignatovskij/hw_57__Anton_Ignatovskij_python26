
from django import forms
from django.forms import widgets


from issue_tracker.models import Project, Task, Status, Type
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


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'beginning_date', 'ending_date')
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'beginning_date': 'Дата начала',
            'ending_date': 'Дата окончания',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'beginning_date': forms.DateInput(
                format='%Y-%m-%d', attrs={'type': 'date'},
            ),
            'ending_date': forms.DateInput(
                format='%Y-%m-%d', attrs={'type': 'date'},
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        beginning_date = cleaned_data.get('beginning_date')
        ending_date = cleaned_data.get('ending_date')
        if beginning_date and ending_date and ending_date < beginning_date:
            self.add_error('ending_date', 'Дата окончания не может быть раньше даты начала.')
        return cleaned_data


class SimpleSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        label="Поиск проектов",
        widget=forms.TextInput(attrs={
            'type': 'search',
            'class': 'form-control',
            'placeholder': 'Название или описание проекта',
        }),
    )
