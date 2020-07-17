from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone


def user_profilepics_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'static/profilepics/user_{0}/{1}'.format(instance.user.id, filename)


class Member(AbstractUser):
    GENDER_CHOICE = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('-', 'Preferred Not to Mention'),
    ]
    email = models.EmailField(null=False, blank=False)
    nickname = models.CharField(max_length=50, default=' ', null=True, blank=True)
    companion_email = models.EmailField('companion_email', blank=True)
    companion_name = models.CharField(max_length=100, default=' ', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, null=False, blank=False, default='-')
    profile_pic = models.CharField(max_length=100,
                                   default="static/manage_sy/profilepics/profile_avatar_contact_account_user_default-neutral.png",
                                   blank=True)
    is_first_registered = models.BooleanField(default=True)
    companion_registered = models.BooleanField(default=False)
    companion_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    home_name = models.CharField(max_length=100, default=' ', null=True, blank=True)


class SyItem(models.Model):
    ITEM_TYPE = [
        ('R', 'Request For'),
        ('C', 'Confess It'),
    ]
    RESPONSE_TYPE = [
        ('Y', 'Accepted'),
        ('N', 'Rejected'),
    ]
    HAPPENED_ON_CHOICE = [
        ('t', 'Today'),
        ('y', 'Yesterday'),
        ('w', 'A week ago'),
        ('m', 'Around a month ago'),
        ('Y', 'An year ago'),
        ('-', 'I don''t really remember'),
    ]
    name = models.CharField(max_length=500, blank=False, null=False, default=' ')
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    assigned_to = models.CharField(max_length=100, default=' ')
    type = models.CharField(max_length=10, choices=ITEM_TYPE, null=False, blank=False, default= 'R')
    happened_on = models.CharField(max_length=10, choices=HAPPENED_ON_CHOICE, null=False, blank=False, default='-')
    created_date = models.DateTimeField(
        default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=10, choices=ITEM_TYPE, null=True, blank=True)
    active = models.BooleanField(default=False)
    image_clue = models.CharField(max_length=1000,
                                   default="static/manage_sy/profilepics/profile_avatar_contact_account_user_default-neutral.png",
                                   blank=True)
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


