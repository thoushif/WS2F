from django.urls import path
from django.conf.urls import url
from .views import SignUpView, MemberDetailView, MemberUpdateView, MemberUpdateCompanionView, CardsInboxView, \
    CardsPostedView, sy_item_modal_view, send_remind_email, SyItemCreateView, SyItemUpdateView, CompanionDetailView, sy_item_accept_view, sy_item_reject_view
from django.views.generic.base import TemplateView
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'manage_sy'
urlpatterns = [
    # path('', views.index, name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('users/<int:pk>/edit/',
         MemberUpdateView.as_view(), name='member_edit'),
    path('users/<int:pk>/edit_add_companion/',
         MemberUpdateCompanionView.as_view(), name='member_edit_add_companion'),
    path('cards/',
         CardsInboxView.as_view(), name='cards_for_you'),
    path('cards-by-you/',
         CardsPostedView.as_view(), name='cards_by_you'),
    path('modal/item-detail/', sy_item_modal_view, name='item_detail'),
    path('modal/item-new/', SyItemCreateView.as_view(), name='item_new'),
    path('item-accept/<int:pk>/', sy_item_accept_view, name='item_accept'),
    path('item-reject/<int:pk>/', sy_item_reject_view, name='item_reject'),
    path('modal/item-edit/<int:pk>/', SyItemUpdateView.as_view(), name='item_edit'),
    # path('modal/item-edit/', SyItemUpdateView2.as_view(), name='item_edit2'),
    # path('modal/item-edit/<int:pk>/', syitem_edit, name='item_edit'),
    path('user/<int:pk>',
         MemberDetailView.as_view(), name='member_detail'),
    path('companion/<int:pk>',
         CompanionDetailView.as_view(), name='companion_detail'),
    # path('users/new/', MemberCreateView.as_view(), name='client_new'),
    path('users/remind/', send_remind_email, name='companion_remind'),
    path('password-reset-form/', PasswordResetView.as_view(), name='password_reset_form'),
    path('password-reset-done-form/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm')


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)