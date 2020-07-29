from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import logout, authenticate, login
from django import forms
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView, FormView
from .forms import MemberCreationForm, MemberCreationForm2,MemberCreationForm3, SyItemForm, SyItemFormCreate
from .models import Member, SyItem
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .utils import findNewcompanion_inv_code
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


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
            orig_member = Member.objects.filter(
                companion_email=email_id).first()
            orig_member.companion_registered = True
            member.companion_registered = True
            orig_member.companion_id = member
            member.companion_id = orig_member
            member.is_first_registered = False
            member.home_name = orig_member.home_name
        member.save()
        if orig_member is not None:
            orig_member.save()

        # send_email([email_id])
        return HttpResponseRedirect('/')



class SignUpView2(CreateView):
    form_class = MemberCreationForm2
    template_name = 'signup.html'
    

    def form_valid(self, form):
        member = form.save(commit=False)
        email_id = form.cleaned_data.get('email')
                # default first user.
        member.companion_registered = False
        member.is_first_registered = False
        member.companion_invitation_code = findNewcompanion_inv_code()
        member.companion_name=None
        member.save()
        

        send_email(member,[email_id],True)
        login(self.request,member)
        return HttpResponseRedirect('/')


class SignUpView3(CreateView):
    form_class = MemberCreationForm3
    template_name = 'signup.html'
    
    def get_initial(self):
        logout(self.request)
        
        initial = super().get_initial()
        initial['companion_invitation_code'] = self.kwargs.get('slug')
        member = Member.objects.filter(companion_invitation_code=self.kwargs.get('slug')).first()
        if member is not None and not member.companion_registered:
             initial['email'] = member.companion_email
             initial['nickname'] = member.companion_name
             initial['username'] = member.companion_name
             initial['home_name'] = member.home_name
        else:
            initial['companion_invitation_code'] = self.kwargs.get('slug') +" code not active, guess you might signup with out code (or) ask your companion to give a correct code"
        return initial

    def form_valid(self, form):
        member = form.save(commit=False)
        email_id = form.cleaned_data.get('email')
        orig_member = None
        # if there is a orig member

        if Member.objects.filter(companion_email=email_id).exists():
            orig_member = Member.objects.filter(companion_email=email_id).first()

            orig_member.companion_id = member
            orig_member.companion_registered = True
            orig_member.companion_name = member.username
            orig_member.is_first_registered = True
            orig_member.companion_email = email_id

            member.companion_registered = True
            member.companion_id = orig_member
            member.is_first_registered = False
            member.companion_name = orig_member.username
            member.companion_email=orig_member.email


        member.save()
        if orig_member is not None:
            orig_member.save()

        send_email(member,[email_id],False)
        login(self.request,member)
        return HttpResponseRedirect('/')


def get_cards(user_id, slug, isCompanionFlow):
    syObjects_filtered = None
    thisUser = Member.objects.filter(id=user_id).first()
    if thisUser is None:
        return None, 0, 0, 0
    if isCompanionFlow:
        thisUser = Member.objects.filter(companion_id_id=user_id).first(
        ) or Member.objects.filter(id=user_id).first()
        syObjects = SyItem.objects.filter(active=True, owner=thisUser.id)
    else:
        thisUser = Member.objects.filter(id=user_id).first()
        syObjects = SyItem.objects.filter(owner=user_id)

    if thisUser is not None:
        syObjects_filtered = filterBySlug(thisUser, syObjects, slug)
    
    adminUser = Member.objects.filter(username='apologyadmin').first()
    syObjectsAdmin = SyItem.objects.filter(owner=adminUser).all()
    print('syObjectsBefore.count()',syObjects.count())
    print('syObjectsAdmin.count()',syObjectsAdmin.count())
    syObjects.union(syObjects, syObjectsAdmin)
    print('syObjectsAfter.count()',syObjects.count())

    print('syObjects_filteredBefore.count()',syObjects_filtered.count())
    syObjects_filtered.union(syObjects_filtered,syObjectsAdmin)
    print('syObjects_filteredAfter.count()',syObjects_filtered.count())

    return syObjects_filtered, syObjects.filter(active=True).count(), syObjects.filter(active=False).count(), filterBySlug(thisUser, syObjects, 'to-respond').count()


def filterBySlug(thisUser, sybojects, slug):
    print("working with slug", slug)
    if slug == 'accepted':
        sybojects = sybojects.filter(owner_id=thisUser.id, response_type='Y')
    elif slug == 'rejected':
        sybojects = sybojects.filter(owner_id=thisUser.id, response_type='N')
    elif slug == 'drafts':
        sybojects = sybojects.filter(
            owner_id=thisUser.id, active=False, response_type=None)
    elif slug == 'to-respond':
        sybojects = sybojects.filter(
            owner_id=thisUser.id, active=True, response_type=None)
    elif slug is None:
        # inbox view only for those which are sent(active)
        sybojects = sybojects.filter(owner_id=thisUser.id)
    return sybojects


def send_companion_remind_email(request):
    email = Member.objects.filter(id=request.user.id).first().companion_email
    remind_email(request.user,[email], request.user.email)
    messages.success(request, "Reminder sent successfully!")
    # return redirect(reverse('manage_sy:cards_by_you'))
    return redirect(reverse('manage_sy:cards_for_you'))


def send_card_remind_email(request):
    print('#####################im here############################################')
    email = Member.objects.filter(id=request.user.id).first().companion_email
    # remind_email([email], request.user.email)
    messages.success(request, "Reminder for this card sent successfully!")
    return redirect(reverse('manage_sy:cards_by_you_slug', kwargs={'slug': 'to-respond'}))
    # return render(request, '/manage_sy/cards-by-you/to-respond/')


class CardsInboxView(TemplateView):  # cards for you
    template_name = 'home.html'
    ordering = ['-updated_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slugPassed = 'to-respond' if  "/"  == self.request.path else self.kwargs.get('slug')
        filtered_companion_cards, all_companion_cards_count, draft_count, to_companion_respond_count = get_cards(
            self.request.user.id, slugPassed, True)
        if filtered_companion_cards is not None:
            context['companion_cards'] = filtered_companion_cards.order_by(
                '-updated_date')
        else:
            context['companion_cards'] = None

        filtered_cards, all_cards_count, draft_count, to_respond_count = get_cards(
            self.request.user.id, slugPassed, False)
        if filtered_cards is not None:
            context['cards'] = filtered_cards.order_by('-updated_date')
        else:
            context['cards'] = None
        context['cards_for_you_flow'] = True
        # context['cards_count'] = "smain %s of %s" % (filtered_cards.count() if filtered_cards else 0,all_cards_count)
        context['to_respond_count'] = "Respond(%s)" % to_companion_respond_count
        context['companion_cards_count'] = "%s of %s" % (filtered_companion_cards.count(
        ) if filtered_companion_cards else 0, all_companion_cards_count)
        context['heading'] = slugPassed if slugPassed is not None else ''
        # print('self.request.user.companion_name',self.request.user.companion_registered)
        if self.request.user.is_authenticated:
            if not self.request.user.companion_registered:
                context['heading'] = ''
        return context


class CardsPostedView(TemplateView):  # cards by you
    template_name = 'home.html'
    ordering = ['-updated_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_companion_cards, all_companion_cards_count, draft_count, to_respond_count = get_cards(
            self.request.user.id, self.kwargs.get('slug'), True)
        if filtered_companion_cards is not None:
            context['companion_cards'] = filtered_companion_cards.order_by(
                '-updated_date')
        else:
            context['companion_cards'] = None
        filtered_cards, all_cards_count, draft_count, to_respond_count = get_cards(
            self.request.user.id, self.kwargs.get('slug'), False)
        if filtered_cards is not None:
            context['cards'] = filtered_cards.filter(
                active=True).order_by('-updated_date')
        else:
            context['cards'] = None
        context['cards_for_you_flow'] = False
        context['draft_count'] = "Drafts(%s)" % draft_count
        if self.kwargs.get('slug') == 'drafts':
            cards_count_message = "%s, Sent - %s" % (
                draft_count, all_cards_count)
            context['cards'] = filtered_cards.order_by('-updated_date')

        else:
            cards_count_message = "%s of %s" % (filtered_cards.filter(
                active=True).count() if filtered_cards else 0, all_cards_count)

        context['cards_count'] = cards_count_message
        # context['companion_cards_count'] = " companion  %s of %s" % (filtered_companion_cards.count()  if filtered_companion_cards else 0,all_companion_cards_count)
        context['heading'] = self.kwargs.get(
            'slug') if self.kwargs.get('slug') is not None else ''

        return context


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
        companion = Member.objects.filter(
            companion_id_id=self.request.user.id).first()
        context['isCompanionProfile'] = True
        context['companion_name'] = companion.username
        context['companion_home'] = self.request.user.home_name
        return context


class MemberUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Member
    fields = (
        'nickname', 'gender', 'profile_pic', 'home_name')

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

    def get_success_url(self):
        return reverse('home')

    def has_permission(self):
        return self.request.user.id == self.kwargs['pk']


def sy_item_modal_view(request):
    if request.method == 'POST' and request.is_ajax():
        ID = request.POST.get('id')
        sy_item = SyItem.objects.get(pk=ID)  # So we send the item instance
    html = render_to_string('includes/modal-sent.html',
                            {'item': sy_item, 'user_id': request.user.id})
    return HttpResponse(html)


def sy_item_accept_view(request, pk):
    sy_item = SyItem.objects.get(pk=pk)
    sy_item.response_type = 'Y'
    sy_item.response_date = timezone.now()
    sy_item.color = 'bg-success'
    sy_item.save()
    messages.success(request, sy_item.name + " accepted!!")
    return redirect(reverse('manage_sy:cards_for_you_slug', kwargs={'slug': 'to-respond'}))


def sy_item_reject_view(request, pk):
    sy_item = SyItem.objects.get(pk=pk)
    sy_item.response_type = 'N'
    sy_item.response_date = timezone.now()
    sy_item.color = 'bg-danger'
    sy_item.save()
    messages.success(request, sy_item.name + " rejected!!")
    # return HttpResponse(render(request, 'home.html'))
    return redirect(reverse('manage_sy:cards_for_you_slug', kwargs={'slug': 'to-respond'}))


def sy_item_save_view(request, pk):
    sy_item = SyItem.objects.get(pk=pk)
    sy_item.active = True
    sy_item.save()
    messages.success(request, sy_item.name + " sent successfully!!")
    return redirect(reverse('manage_sy:cards_by_you_slug', kwargs={'slug': 'drafts'}))


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


class SyItemCreateView(FormView):
    template_name = 'includes/modal-new-item-form.html'
    form_class = SyItemFormCreate

    def get_form_kwargs(self):
        kwargs = super(SyItemCreateView, self).get_form_kwargs()
        print("##########################", self.kwargs.get('slug'))
        kwargs['types'] = self.kwargs.get('slug')
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        sy_item = form.save(commit=False)
        sy_item.owner = Member.objects.filter(id=self.request.user.id).first()
        sy_item.active = False
        sy_item.color = sy_item.type
        sy_item.assigned_to = Member.objects.filter(
            id=self.request.user.id).first().companion_name
        sy_item.save()
        # return HttpResponse(render(self.request, '/manage_sy/cards-by-you/drafts'))
        # return render(self.request,  '/manage_sy/cards-by-you/drafts', self.get_context_data())
        return redirect(reverse('manage_sy:cards_by_you_slug', kwargs={'slug': 'drafts'}))


class SyItemCreateView2(FormView):
    template_name = 'includes/modal-new-item-form.html'
    form_class = SyItemFormCreate

    def form_valid(self, form):
        print("###############", self.kwargs.get('slug'))
        form.instance.author = self.request.user
        sy_item = form.save(commit=False)
        sy_item.owner = Member.objects.filter(id=self.request.user.id).first()
        sy_item.active = False
        sy_item.color = sy_item.type
        sy_item.type = self.kwargs.get('slug')
        sy_item.assigned_to = Member.objects.filter(
            id=self.request.user.id).first().companion_name
        sy_item.save()
        # return HttpResponse(render(self.request, '/manage_sy/cards-by-you/drafts'))
        # return render(self.request,  '/manage_sy/cards-by-you/drafts', self.get_context_data())
        return redirect(reverse('manage_sy:cards_by_you_slug', kwargs={'slug': 'drafts'}))


class SyItemUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SyItem
    # form = SyItemForm(instance=get_object_or_404(SyItem))
    template_name = 'includes/modal-update-item-form.html'
    fields = ('name', 'type', 'happened_on', 'notes',)
    success_url = '/manage_sy/cards-by-you/'
    success_message = "Item updated successfully"

    def form_valid(self, form):
        return super().form_valid(form)


def send_email(member, recipient_list, first_joined):
    # subject = 'Thank you for registering to our site'
    # message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    # send_mail(subject, message, email_from, recipient_list)
    subject = 'Thanks for signinup at All About Apology - its all yours now!'
    html_message = render_to_string('email-templates/user-signup-thanks.html', {'member': member,'first_joined':first_joined})
    plain_message = strip_tags(html_message)

    mail.send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)



def remind_email(user,recipient_list, myemail):
    email_from = settings.EMAIL_HOST_USER
    # send_mail(subject, message, email_from, recipient_list)
        
    subject = 'Sign up here at All About Apology - <invitation code included>'
    html_message = render_to_string('email-templates/companion_invite.html', {'user': user})
    plain_message = strip_tags(html_message)

    mail.send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)
