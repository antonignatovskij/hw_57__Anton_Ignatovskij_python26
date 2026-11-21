from django import forms
from django.contrib.auth.models import User
from issue_tracker.models import Project

class MemberAddForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('members',)
        widgets = {
            'members': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_members = self.instance.members.values_list('pk', flat=True)
        self.fields['members'].queryset = User.objects.exclude(pk__in=current_members)
