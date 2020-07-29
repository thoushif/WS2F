from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Member, SyItem


class MemberCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Member
        fields = ('username', 'email', 'first_name', 'last_name', 'nickname', 'companion_email', 'companion_name', 'gender', 'home_name')
        widgets = {
            'gender': forms.RadioSelect()
        }

    def clean_email(self):
        if Member.objects.filter(email=self.cleaned_data.get('email')).exists():
            raise forms.ValidationError("Email is already registered, try Forgot Password if this email is yours!")
        return self.cleaned_data.get('email')

class MemberCreationForm2(UserCreationForm):

    class Meta(UserCreationForm):
        model = Member
        fields = ('username', 'email', 'first_name', 'last_name', 'nickname', 'gender', 'home_name')

    def clean_email(self):
        if Member.objects.filter(email=self.cleaned_data.get('email')).exists():
            raise forms.ValidationError("Email is already registered, try Forgot Password if this email is yours!")
        return self.cleaned_data.get('email')


class MemberCreationForm3(UserCreationForm):

    class Meta(UserCreationForm):
        model = Member
        fields = ('companion_invitation_code', 'username', 'email', 'first_name', 'last_name', 'nickname', 'gender', 'home_name')
        widgets = {
            'companion_invitation_code': forms.TextInput(attrs={'disabled': 'disabled'}),
            # 'email': forms.EmailInput(attrs={'disabled': 'disabled'}),
        }


    def clean_email(self):
        if Member.objects.filter(email=self.cleaned_data.get('email')).exists():
            raise forms.ValidationError("Email is already registered, try Forgot Password if this email is yours!")
        return self.cleaned_data.get('email')



class MemberChangeForm(UserChangeForm):

    class Meta:
        model = Member
        fields = ('companion_invitation_code', 'username', 'email', 'first_name', 'last_name', 'nickname', 'gender', 'home_name')
        widgets = {
            'gender': forms.RadioSelect()
        }


class SyItemForm(forms.ModelForm):

    class Meta:
        model = SyItem
        fields = ('name', 'assigned_to', 'type', 'happened_on', 'created_date', 'color', 'active', 'notes', 'owner', )

 
class SyItemFormCreate(forms.ModelForm):

    class Meta:
        model = SyItem
        fields = ('name', 'happened_on', 'notes',)
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'This happened...'}),
            'notes':forms.Textarea(attrs={'placeholder': 'you know what...','rows':3}),
        }

    # def __init__(self, *args, **kwargs): 
    #     type = kwargs.pop('types', None) # pop the 'type' from kwargs dictionary      
    #     super(SyItemFormCreate, self).__init__(*args, **kwargs)
    #     print("@@@@@@@@before@@@@@@@@@@@@@@@@@@@@@",self.fields['type'].initial)   
    #     print("@@@@@@@@slug@@@@@@@@@@@@@@@@@@@@@",type)   

    #     self.fields['type'] = forms.TypedChoiceField(choices=SyItem.ITEM_TYPE, initial='C')
    #     print("@@@@@@@@after@@@@@@@@@@@@@@@@@@@@@",self.fields['type'])   
