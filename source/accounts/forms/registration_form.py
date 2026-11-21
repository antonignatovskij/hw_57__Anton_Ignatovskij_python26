from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')

    def clean(self):
        cleaned_data = super().clean()
        first = cleaned_data.get('first_name')
        last = cleaned_data.get('last_name')

        if not first and not last:
            raise ValidationError('Заполните имя или фамилию.')

        return cleaned_data
