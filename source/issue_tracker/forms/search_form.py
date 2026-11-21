from django import forms

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