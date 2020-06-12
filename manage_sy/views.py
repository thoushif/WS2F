from django.utils import timezone

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import logout
from django import forms
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from .forms import MemberCreationForm, SyItemForm
from .models import Member, SyItem
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings


def index(request):
    return HttpResponse("Hello, world. You're at the manage_sy index.")


class SignUpView(CreateView):
    form_class = MemberCreationForm
    template_name = 'signup.html'

    def form_valid(self, form):
        member = form.save(commit=False)
        email_id = form.cleaned_data.get('email')
        # check if this email id is any companion's email
        orig_member = None
        if Member.objects.filter(companion_email=email_id).exists():
            orig_member = Member.objects.filter(companion_email=email_id).first()
            orig_member.companion_registered = True
            member.companion_registered = True
            orig_member.companion_id = member
            member.companion_id = orig_member
            member.is_first_registered = False
            member.home_name = orig_member.home_name
        member.save()
            if orig_member is not None:
        orig_member.save()


        send_email([email_id])
        return HttpResponseRedirect('/')


def get_companion_cards(user_id):
    companion = Member.objects.filter(companion_id_id=user_id).first()
    if companion is not None:
        return SyItem.objects.filter(owner_id=companion.id)


def send_remind_email(request):
    email = Member.objects.filter(id=request.user.id).first().companion_email
    remind_email([email])
    messages.success = "Reminder sent successfully!"
    return HttpResponse(render(request, 'home.html'))


class CardsInboxView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companion_cards = get_companion_cards(self.request.user.id)
        if companion_cards is not None:
            context['companion_cards'] = companion_cards.order_by('-updated_date')
        else:
            context['companion_cards'] = None
        context['cards_for_you_flow'] = True
        return context


class CardsPostedView(TemplateView):
    template_name = 'home.html'
    ordering = ['-updated_date']


class MemberDetailView(PermissionRequiredMixin, DetailView):
    model = Member
    template_name = 'member_detail.html'
    login_url = 'login'

    def has_permission(self):
        return self.request.user.id == self.kwargs['pk']


class CompanionDetailView(LoginRequiredMixin, DetailView):
    model = Member
    template_name = 'member_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companion = Member.objects.filter(companion_id_id=self.request.user.id).first()
        context['isCompanionProfile'] = True
        context['companion_name'] = companion.username
        context['companion_home'] = self.request.user.home_name
        return context


class MemberUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Member
    fields = (
         'nickname', 'date_of_birth', 'gender', 'profile_pic', 'home_name')
    template_name = 'member_edit.html'
    success_message = "Profile saved successfully"

    def get_success_url(self):
        return reverse('home')

    def has_permission(self):
        return self.request.user.id == self.kwargs['pk']


class MemberUpdateCompanionView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Member
    fields = (
         'companion_name', 'companion_email')
    template_name = 'member_edit.html'
    success_message = "Companion added successfully, they may have to register if not already do so!!"

    def get_success_url(self):
        return reverse('home')

    def has_permission(self):
        return self.request.user.id == self.kwargs['pk']

def sy_item_modal_view(request):
    if request.method == 'POST' and request.is_ajax():
        ID = request.POST.get('id')
        sy_item = SyItem.objects.get(pk=ID)  # So we send the item instance
    html = render_to_string('includes/modal-sent.html', {'item': sy_item, 'user_id': request.user.id})
    return HttpResponse(html)


def sy_item_accept_view(request, pk):
    sy_item = SyItem.objects.get(pk=pk)
    sy_item.response_type = 'Y'
    sy_item.response_date = timezone.now()
    sy_item.color = 'bg-success'
    sy_item.save()
    messages.success = sy_item.name + "Accepted!!"
    return HttpResponse(render(request, 'home.html'))


def sy_item_reject_view(request, pk):
    sy_item = SyItem.objects.get(pk=pk)
    sy_item.response_type = 'N'
    sy_item.response_date = timezone.now()
    sy_item.color = 'bg-danger'
    sy_item.save()
    return HttpResponse(render(request, 'home.html'))


def handler400(request, exception, template_name="400.html"):
    response = render(request, template_name)
    response.status_code = 400
    return response


def handler403(request, exception, template_name="403.html"):
    response = render(request, template_name)
    response.status_code = 403
    return response


def handler404(request, exception, template_name="404.html"):
    response = render(request, template_name)
    response.status_code = 404
    return response


def handler500(request, template_name="500.html"):
    response = render(request, template_name)
    response.status_code = 500
    return response

# class SyItemUpdateView(UpdateView):
#     model = SyItem
#     form_class = SyItemForm
#     template_name = 'item_edit_form.html'
#
#     def dispatch(self, *args, **kwargs):
#         self.item_id = kwargs['pk']
#         return super(SyItemUpdateView, self).dispatch(*args, **kwargs)
#
#     def form_valid(self, form):
#         form.save()
#         item = SyItem.objects.get(id=self.item_id)
#         return HttpResponse(render_to_string('item_edit_form_success.html', {'syitem': item}))


class SyItemCreateView(CreateView):
    model = SyItem
    success_url = '/manage_sy/modal/item-new/'
    template_name = 'includes/modal-new-item-form.html'
    fields = ('type', 'subType', 'name', 'happened_on', 'notes',)

    widgets = {
        'type': forms.RadioSelect()
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        sy_item = form.save(commit=False)
        sy_item.owner = Member.objects.filter(id=self.request.user.id).first()
        sy_item.active = True
        sy_item.color = sy_item.type
        sy_item.assigned_to = Member.objects.filter(id=self.request.user.id).first().companion_name
        sy_item.save()
        return HttpResponse(render(self.request, 'home.html'))


class SyItemUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SyItem
    # form = SyItemForm(instance=get_object_or_404(SyItem))
    template_name = 'includes/modal-update-item-form.html'
    fields = ('name', 'type', 'happened_on', 'image_clue', 'notes', 'subType')
    success_url = '/'
    success_message = "Item updated successfully"

    def form_valid(self, form):
        return super().form_valid(form)


def send_email(recipient_list):
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, recipient_list )


def remind_email(recipient_list):
    subject = 'Reminder: Sign up here please at AAA - we can have our fun back'
    message = ' Dear, I hope you join this site signing up. I feel this help us  connecting back in our lives. Even i' \
              'f not lets have fun.  '
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, recipient_list )
