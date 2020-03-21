from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Member, SyItem


class MemberCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Member
        fields = ('username', 'email', 'nickname', 'date_of_birth', 'companion_email', 'companion_name', 'gender', 'profile_pic', 'home_name')


class MemberChangeForm(UserChangeForm):

    class Meta:
        model = Member
        fields = ('username', 'email', 'nickname', 'date_of_birth', 'companion_email', 'companion_name', 'gender', 'profile_pic', )


class SyItemForm(forms.ModelForm):

    class Meta:
        model = SyItem
        fields = ('name', 'assigned_to', 'type', 'happened_on', 'created_date', 'color', 'active', 'image_clue', 'notes', 'owner', 'subType', )