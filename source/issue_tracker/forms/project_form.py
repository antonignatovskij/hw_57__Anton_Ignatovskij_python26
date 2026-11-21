from django import forms
from issue_tracker.models import Project


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
