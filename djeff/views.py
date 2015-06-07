from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Contact
import logging
logger = logging.getLogger(__name__)

def hello_world(request):
    print 'hello'
    print logger.name
    logger.info('hello logging')
    return HttpResponse("Hello, World")
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from django.views.generic import View

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
class ContactOwnerMixin(object):

    def get_object(self, queryset=None):
        """Returns the object the view is displaying.

        """

        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg, None)
        queryset = queryset.filter(
            pk=pk,
            owner=self.request.user,
        )

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise PermissionDenied

        return obj
class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)
class LoggingMixin(object):

    def dispatch(self, *args, **kwargs):
        logger.info('logging from mixin')
        return super(LoggingMixin, self).dispatch(*args, **kwargs)

class MyView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, World from class view")


from django.views.generic import ListView

from django.contrib.auth.models import User
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

from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from .forms import ContactForm, ContactAddressFormSet


class CreateContactView(LoggedInMixin,CreateView):
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
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CreateContactView, self).form_valid(form)

from django.views.generic import UpdateView


class UpdateContactView(LoggedInMixin,ContactOwnerMixin,UpdateView):
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


class DeleteContactView(LoggedInMixin,ContactOwnerMixin,DeleteView):
    model = Contact
    template_name = 'delete_contact.html'

    def get_success_url(self):
        return reverse('list')


from django.views.generic import DetailView


class ContactView(LoggingMixin, DetailView):
    model = Contact
    template_name = 'contact.html'



class EditContactAddressView(LoggedInMixin,ContactOwnerMixin, UpdateView):

    model = Contact
    template_name = 'edit_addresses.html'
    form_class = ContactAddressFormSet
    def get_success_url(self):
        return self.get_object().get_absolute_url()
