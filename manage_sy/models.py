from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Member(AbstractUser):
    GENDER_CHOICE = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('-', 'Preferred Not to Mention'),
    ]
    nickname = models.CharField(max_length=50, default=' ', null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)  # True makes this field optional
    companion_email = models.EmailField('companion_email', blank=True)
    companion_name = models.CharField(max_length=100, default=' ', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, null=True, blank=True)
    profile_pic = models.CharField(max_length=100,
                                   default="static/manage_sy/profilepics/profile_avatar_contact_account_user_default-neutral.png",
                                   blank=True)
    is_first_registered = models.BooleanField(default=True)
    companion_registered = models.BooleanField(default=False)
    companion_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    home_name = models.CharField(max_length=100, default=' ', null=True, blank=True)


class ItemSubTypeDomain(models.Model):
    ITEM_TYPE = [
        ('R', 'Request For'),
        ('C', 'Confess It'),
    ]
    type = models.CharField(max_length=10, choices=ITEM_TYPE, null=True, blank=True)
    subType = models.CharField(max_length=100)


class SyItem(models.Model):
    ITEM_TYPE = [
        ('R', 'Request For'),
        ('C', 'Confess It'),
    ]
    RESPONSE_TYPE = [
        ('Y', 'Accepted'),
        ('N', 'Rejected'),
    ]
    name = models.CharField(max_length=500, blank=False, null=False, default=' ')
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    assigned_to = models.CharField(max_length=100, default=' ')
    type = models.CharField(max_length=10, choices=ITEM_TYPE, null=True, blank=True)
    happened_on = models.DateField(blank=True, null=True)  # True makes this field optional
    created_date = models.DateTimeField(
        default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=10, choices=ITEM_TYPE, null=True, blank=True)
    active = models.BooleanField(default=False)
    image_clue = models.CharField(max_length=1000,
                                   default="static/manage_sy/profilepics/profile_avatar_contact_account_user_default-neutral.png",
                                   blank=True)
    subType = models.ForeignKey(ItemSubTypeDomain, on_delete=models.DO_NOTHING, related_name='request_types')

    notes = models.TextField()
    response_type = models.CharField(max_length=10, choices=RESPONSE_TYPE, null=True, blank=True)
    response_date = models.DateTimeField(auto_now_add=True, null=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name


