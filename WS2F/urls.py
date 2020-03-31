"""WS2F URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from manage_sy.views import CardsInboxView


handler404 = 'manage_sy.views.handler404'
handler500 = 'manage_sy.views.handler500'
handler403 = 'manage_sy.views.handler403'
handler400 = 'manage_sy.views.handler400'

urlpatterns = [
    path('', CardsInboxView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('manage_sy/', include('manage_sy.urls')),
    path('manage_sy/', include('django.contrib.auth.urls')),
]