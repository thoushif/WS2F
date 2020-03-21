from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import MemberCreationForm, MemberChangeForm
from .models import Member, SyItem, ItemSubTypeDomain


class SyItemInline(admin.TabularInline):
    model = SyItem
    extra = 2


class MemberAdmin(UserAdmin):
    add_form = MemberCreationForm
    form = MemberChangeForm
    model = Member
    list_display = ['email', 'username', 'nickname', 'gender', 'companion_email', 'companion_name', 'profile_pic', ]
    inlines = [SyItemInline]


class SyItemAdmin(admin.ModelAdmin):
    model = SyItem
    list_display = ['name', 'owner', 'assigned_to', 'type', 'happened_on', 'created_date', 'updated_date', 'color', 'active', 'image_clue', 'subType', 'notes', ]


admin.site.register(Member, MemberAdmin)
admin.site.register(SyItem, SyItemAdmin)
admin.site.register(ItemSubTypeDomain)
