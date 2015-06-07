# coding=utf-8
from django.test import TestCase
from djeff.models import Contact


class ContactTests(TestCase):
    """Contact model tests."""

    def test_str(self):
        contact = Contact(first_name='John', last_name='Smith')

        self.assertEquals(
            str(contact),
            'John Smith',
        )


from django.test.client import Client
from django.test.client import RequestFactory
from .views import ListContactView


class ContactListViewTests(TestCase):
    """Contact list view tests."""

    def test_contacts_in_the_context(self):
        client = Client()
        response = client.get('/list')

        self.assertEquals(list(response.context['object_list']), [])

        Contact.objects.create(first_name='foo', last_name='bar')
        response = client.get('/list')
        self.assertEquals(response.context['object_list'].count(), 1)

    def test_contacts_in_the_context_request_factory(self):
        factory = RequestFactory()
        request = factory.get('/')

        # 手动绑定view
        response = ListContactView.as_view()(request)

        self.assertEquals(list(response.context_data['object_list']), [])

        Contact.objects.create(first_name='foo', last_name='bar')
        response = ListContactView.as_view()(request)
        self.assertEquals(response.context_data['object_list'].count(), 1)


from rebar.testing import flatten_to_dict
from .forms import ContactForm
class EditContactFormTests(TestCase):

    def test_mismatch_email_is_invalid(self):

        form_data = flatten_to_dict(ContactForm())
        form_data['first_name'] = 'Foo'
        form_data['last_name'] = 'Bar'
        form_data['email'] = 'foo@example.com'
        form_data['confirm_email'] = 'bar@example.com'

        bound_form = ContactForm(data=form_data)
        self.assertFalse(bound_form.is_valid())

    def test_same_email_is_valid(self):

        form_data = flatten_to_dict(ContactForm())
        form_data['first_name'] = 'Foo'
        form_data['last_name'] = 'Bar'
        form_data['email'] = 'foo@example.com'
        form_data['confirm_email'] = 'foo@example.com'

        bound_form = ContactForm(data=form_data)
        self.assertTrue(bound_form.is_valid())
        self.assert_(bound_form.is_valid())