# models.py
from django.db import models
from django.contrib.auth.models import User

class Concert(models.Model):
    name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    venue = models.CharField(max_length=100)
    available_tickets = models.IntegerField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='concert_images/')

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    tickets_booked = models.IntegerField()  # Changed from number_of_tickets to tickets_booked
    created_at = models.DateTimeField(auto_now_add=True)


# models.py
from django.db import models

class Concert(models.Model):
    name = models.CharField(max_length=200)
    date_time = models.DateTimeField()  # Use DateTimeField for date and time
    venue = models.CharField(max_length=200)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_tickets = models.IntegerField(default=0)  # Field for available tickets
    image = models.ImageField(upload_to='concert_images/')  # Ensure you have Pillow installed for image handling

    def __str__(self):
        return self.name
    # models.py
class Booking(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)  # Ensure this line is correct
    tickets_booked = models.IntegerField()
    # Add any other fields as necessary

    # models.py
from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    tickets_booked = models.IntegerField()
    status = models.CharField(max_length=20, default='booked')  # Add a status field

    def __str__(self):
        return f"{self.user.username} - {self.concert.name} - {self.tickets_booked} tickets"
    

# models.py
from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    tickets_booked = models.IntegerField()
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)  # Field for QR code image

    def __str__(self):
        return f"{self.user.username} - {self.concert.name} - {self.tickets_booked} tickets"