import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (dfault 3 weeks).")

    # validate renewal date field
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # check if the date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('nvalid date - renewal more than 4 weeks ahead'))