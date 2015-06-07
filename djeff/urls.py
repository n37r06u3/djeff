"""djeff URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from .views import hello_world, MyView, ListContactView, CreateContactView, \
    UpdateContactView, DeleteContactView,ContactView,EditContactAddressView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
urlpatterns = [
    url(r'^hello$', hello_world, name='home'),
    url(r'^hello2$', MyView.as_view(), name='home2'),
    url(r'^$', ListContactView.as_view(), name='list'),
    url(r'^create$', CreateContactView.as_view(), name='create'),
    url(r'^edit/(?P<pk>\d+)/$', UpdateContactView.as_view(),
        name='edit',),
    url(r'^delete/(?P<pk>\d+)/$', DeleteContactView.as_view(),
        name='delete',),
      url(r'^(?P<pk>\d+)/$', ContactView.as_view(),
        name='view',),
    url(r'^edit/(?P<pk>\d+)/addresses$', EditContactAddressView.as_view(),
        name='edit-addresses',),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url('^register/', CreateView.as_view(
            template_name='register.html',
            form_class=UserCreationForm,
            success_url='/'
    )),
    url('^accounts/', include('django.contrib.auth.urls')),
]
