from django import forms
from django.core.exceptions import ValidationError

from .models import Contact,Address

class ContactForm(forms.ModelForm):

    confirm_email = forms.EmailField(
        label="Confirm email",
        required=True,
    )

    class Meta:
        model = Contact
        #fields = '__all__'
        exclude = ('owner',)
    def __init__(self, *args, **kwargs):
        #if kwargs.get('instance'):
        #    email = kwargs['instance'].email
        #    kwargs.setdefault('initial', {})['confirm_email'] = email

        super(ContactForm, self).__init__(*args, **kwargs)

    def clean(self):
        if (self.cleaned_data.get('email') !=
            self.cleaned_data.get('confirm_email')):
            raise ValidationError(
                "Email addresses must match."
            )
        return self.cleaned_data


from django.forms.models import inlineformset_factory


# inlineformset_factory creates a Class from a parent model (Contact)
# to a child model (Address)
ContactAddressFormSet = inlineformset_factory(
    Contact,
    Address,
    fields= '__all__'
)