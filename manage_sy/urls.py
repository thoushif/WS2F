from django.urls import path
from django.conf.urls import url
from .views import SignUpView, MemberDetailView, MemberUpdateView, MemberCreateView, CardsInboxView, \
    CardsPostedView, sy_item_modal_view, SyItemCreateView, SyItemUpdateView, SyItemUpdateView2, CompanionDetailView, sy_item_accept_view, sy_item_reject_view
from django.views.generic.base import TemplateView

app_name = 'manage_sy'
urlpatterns = [
    # path('', views.index, name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('users/<int:pk>/edit/',
         MemberUpdateView.as_view(), name='member_edit'),
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
]
