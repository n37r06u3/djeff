from django.http import HttpResponse
from .models import Contact


def hello_world(request):
    return HttpResponse("Hello, World")


from django.views.generic import View


class MyView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, World from class view")


from django.views.generic import ListView


class ListContactView(ListView):
    model = Contact


from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from .forms import ContactForm, ContactAddressFormSet


class CreateContactView(CreateView):
    model = Contact
    template_name = 'edit_contact.html'

    form_class = ContactForm
    #fields = '__all__'

    def get_success_url(self):
        return reverse('list')

    def get_context_data(self, **kwargs):
        context = super(CreateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('create')

        return context


from django.views.generic import UpdateView


class UpdateContactView(UpdateView):
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


class DeleteContactView(DeleteView):
    model = Contact
    template_name = 'delete_contact.html'

    def get_success_url(self):
        return reverse('list')


from django.views.generic import DetailView


class ContactView(DetailView):
    model = Contact
    template_name = 'contact.html'



class EditContactAddressView(UpdateView):

    model = Contact
    template_name = 'edit_addresses.html'
    form_class = ContactAddressFormSet
    def get_success_url(self):
        return self.get_object().get_absolute_url()
