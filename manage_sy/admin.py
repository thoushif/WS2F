from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import MemberCreationForm, MemberChangeForm, SyItemForm
from .models import Member, SyItem


class SyItemInline(admin.TabularInline):
    model = SyItem
    extra = 0

class MemberAdmin(UserAdmin):
    add_form = MemberCreationForm
    form = MemberChangeForm
    model = Member
    list_display = ['email', 'username', 'nickname', 'gender', 'companion_email','companion_registered','companion_id', 'companion_invitation_code','companion_name', 'profile_pic', 'home_name', ]
    inlines = [SyItemInline]


class SyItemAdmin(admin.ModelAdmin):
    model = SyItem
    form = SyItemForm
    list_display = [ 'active', 'name', 'owner', 'assigned_to', 'type', 'happened_on', 'created_date', 'updated_date', 'color', 'response_type', 'notes', ]
    list_filter = ('active', 'owner','type','response_type',)


admin.site.register(Member, MemberAdmin)
admin.site.register(SyItem, SyItemAdmin)