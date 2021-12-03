"""contactdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from contact_details.views import *

admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    url(r'^$', contact_list, name='contact_list'),
    url('^oauth/', include('social_django.urls', namespace='social')),
    # path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    # url(r'^contact_list', contact_list, name='contact_list'),
    url(r'^logout/$', auth_logout, name='auth_logout'),
    url(r'^keep_awake/$', keep_awake, name='keep_awake'),
    url(r'^upload_bulk_contacts/$', upload_bulk_contacts, name='upload_bulk_contacts'),
    url(r'^upload_single_contact/$', upload_single_contact, name='upload_single_contact'),
    path('', include('pwa.urls')),
]