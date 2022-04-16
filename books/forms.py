import datetime
from django import forms
from django.core.exceptions import ValidationError

class ReserveBookForm(forms.Form):
    start_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
    def clean_start_date(self):
        date = self.cleaned_data['start_date']
        
        # Check if a date is not in the past.
        if date < datetime.date.today():
            raise ValidationError(_('Invalid date - start in past'))
        
        # Check if a date is in the allowed range (+4 weeks from today).
        if date > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - start date more than 4 weeks ahead'))
        
        return date
    