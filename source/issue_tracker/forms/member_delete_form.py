from django import forms
from issue_tracker.models import Project

class MemberDeleteForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('members',)
        widgets = {
            'members': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_members = self.instance.members
        self.fields['members'].queryset = current_members.all()
        self.initial['members'] = []