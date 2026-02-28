from django import forms
from .models import Celebrity, Booking

class CelebrityForm(forms.ModelForm):
    class Meta:
        model = Celebrity
        fields = '__all__'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['celebrity','status']
