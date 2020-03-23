from django.utils import timezone

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
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
        if Member.objects.filter(companion_email=email_id).exists():
            orig_member = Member.objects.filter(companion_email=email_id).first()
            orig_member.companion_registered = True
            member.companion_registered = True
            orig_member.companion_id = member
            member.companion_id = orig_member
            member.is_first_registered = False
            member.home_name = orig_member.home_name
        member.save()
        orig_member.save()
        sendemail([email_id])
        return HttpResponseRedirect('/')


def get_companion_cards(user_id):
    companion = Member.objects.filter(companion_id_id=user_id).first()
    if companion is not None:
        return SyItem.objects.filter(owner_id=companion.id)


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


class MemberDetailView(LoginRequiredMixin, DetailView):
    model = Member
    template_name = 'member_detail.html'
    login_url = 'login'


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


class MemberUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Member
    fields = (
        'username', 'email', 'nickname', 'date_of_birth', 'companion_email', 'companion_name', 'gender', 'profile_pic', 'home_name')
    template_name = 'member_edit.html'
    success_message = "Profile saved successfully"

    def get_success_url(self):
        return reverse('home')


class MemberCreateView(CreateView):
    model = Member
    template_name = 'member_new.html'
    fields = (
        'username', 'email', 'nickname', 'date_of_birth', 'companion_email', 'companion_name', 'gender', 'profile_pic', 'home_name')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        sendemail(list(self.request.user.sendemail))
        return super().form_valid(form)


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
    sy_item.save()
    messages.success = sy_item.name + "Accepted!!"
    return HttpResponse(render(request, 'home.html'))


def sy_item_reject_view(request, pk):
    sy_item = SyItem.objects.get(pk=pk)
    sy_item.response_type = 'N'
    sy_item.response_date = timezone.now()
    sy_item.save()
    return HttpResponse(render(request, 'home.html'))


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
    fields = ('name', 'type', 'happened_on', 'image_clue', 'notes', 'subType')

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


class SyItemUpdateView2(TemplateView):
    template_name = 'home.html'

def syitem_edit(request, pk):
    sy_item = get_object_or_404(SyItem, pk=pk)
    success_url = 'manage_sy:item_edit'

    if request.method == "POST" and request.is_ajax():
        form = SyItemForm(instance=sy_item)
        print('=============in syitem new with form details')
        print(form.is_valid())
        if form.is_valid():
            print('=============in syitem new with form details in')
            form.save()
            # return super().form_valid(form)
            return HttpResponseRedirect(render(request, 'home.html'))
    else:
        form = SyItemForm(instance=sy_item)
    return render(request, 'includes/modal-update-item-form.html', {'form': form})


def sendemail(recipient_list):
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, recipient_list )
