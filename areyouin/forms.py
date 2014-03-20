from django import forms
from django.contrib.auth.models import User
from bootstrap3_datetime.widgets import DateTimePicker

from areyouin.models import Event

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password')
        
class EventForm(forms.ModelForm):
    event_datetime = forms.DateTimeField(
        widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                       "pickDate": True
                                       }))
    
    class Meta:
        model = Event