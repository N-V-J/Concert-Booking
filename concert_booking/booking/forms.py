from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Booking, Concert

# User Registration Form
class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

# Booking Form
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['concert', 'tickets_booked']

# Ticket Booking Form
class TicketBookingForm(forms.Form):
    number_of_tickets = forms.IntegerField(min_value=1, max_value=3, label="Number of Tickets")

# Concert Form
class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ['name', 'date_time', 'venue', 'ticket_price', 'available_tickets', 'image']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',  # Use HTML5 datetime-local input
            }),
        }

# Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):  # Corrected class name
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')