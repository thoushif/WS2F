from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Member, SyItem


class MemberCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Member
        fields = ('username', 'email', 'first_name', 'last_name', 'nickname', 'date_of_birth', 'companion_email', 'companion_name', 'gender', 'home_name')
        widgets = {
            'gender': forms.RadioSelect()
        }

    def clean_email(self):
        if Member.objects.filter(email=self.cleaned_data.get('email')).exists():
            raise forms.ValidationError("Email is already registered, try Forgot Password if this email is yours!")
        return self.cleaned_data.get('email')


class MemberChangeForm(UserChangeForm):

    class Meta:
        model = Member
        fields = ('username', 'email', 'nickname', 'date_of_birth', 'companion_email', 'companion_name', 'gender', )


class SyItemForm(forms.ModelForm):

    class Meta:
        model = SyItem
        fields = ('subType', 'name', 'assigned_to', 'type', 'happened_on', 'created_date', 'color', 'active', 'notes', 'owner', )

