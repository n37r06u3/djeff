import logging

from django.http import HttpResponse
from django.views.generic import UpdateView
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.contrib.auth.models import User

from .models import Contact
from .mixins import LoggedInMixin, LoggingMixin, ContactOwnerMixin
from .forms import ContactForm, ContactAddressFormSet

logger = logging.getLogger(__name__)


def hello_world(request):
    print 'hello'
    print logger.name
    logger.info('hello logging')
    return HttpResponse("Hello, World")


class MyView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, World from class view")


class ListContactView(ListView):
    model = Contact
    # def get_queryset(self):
    #     if self.request.user.is_authenticated():
    #         qs = Contact.objects.filter(owner=self.request.user)
    #     else:
    #         qs = Contact.objects.all()
    #     return qs

    def get_context_data(self, **kwargs):
        context = super(ListContactView, self).get_context_data(**kwargs)
        context['user_count'] = User.objects.count()
        return context

    def get(self, request, *args, **kwargs):
        logger.info('logging home')
        return super(ListContactView, self).get(request, *args, **kwargs)


class CreateContactView(LoggedInMixin, CreateView):
    model = Contact
    template_name = 'edit_contact.html'

    form_class = ContactForm
    # fields = '__all__'

    def get_success_url(self):
        return reverse('list')

    def get_context_data(self, **kwargs):
        context = super(CreateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('create')
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CreateContactView, self).form_valid(form)


class UpdateContactView(LoggedInMixin, ContactOwnerMixin, UpdateView):
    model = Contact
    template_name = 'edit_contact.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse('list')

    def get_context_data(self, **kwargs):
        context = super(UpdateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('edit',
                                    kwargs={'pk': self.get_object().id})

        return context


from django.views.generic import DeleteView


class DeleteContactView(LoggedInMixin, ContactOwnerMixin, DeleteView):
    model = Contact
    template_name = 'delete_contact.html'

    def get_success_url(self):
        return reverse('list')


class ContactView(LoggingMixin, DetailView):
    model = Contact
    template_name = 'contact.html'


class EditContactAddressView(LoggedInMixin, ContactOwnerMixin, UpdateView):
    model = Contact
    template_name = 'edit_addresses.html'
    form_class = ContactAddressFormSet

    def get_success_url(self):
        return self.get_object().get_absolute_url()
