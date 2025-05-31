from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Concert, Booking
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


# Home view to display all concerts
def home(request):
    concerts = Concert.objects.all().order_by('date_time')  # Fetch all concerts ordered by date
    return render(request, 'home.html', {'concerts': concerts})

# User registration view
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'registration/signup.html')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'registration/signup.html')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)  # Automatically log in the user after registration
        return redirect('login')  # Redirect to home after registration
    else:
        return render(request, 'registration/signup.html')
    
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'registration/login.html')

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Check if the user is the dealer
            if username == 'nvj':  # Replace with your dealer username
                return redirect('dealer')  # Redirect to the Dealer page
            else:
                messages.error(request, 'You do not have access to the Dealer page.')
                return redirect('home')  # Redirect to home or another page
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'registration/login.html')

# Book ticket view
@login_required
def book_ticket(request):
    if request.method == 'POST':
        concert_id = request.POST.get('concert_id')
        number_of_tickets = int(request.POST.get('number_of_tickets', 0))
        concert = get_object_or_404(Concert, id=concert_id)

        if number_of_tickets > concert.available_tickets:
            messages.error(request, "Not enough tickets available.")
        elif number_of_tickets > 3:
            messages.error(request, "You can only book a maximum of 3 tickets.")
        else:
            concert.available_tickets -= number_of_tickets
            concert.save()
            Booking.objects.create(user=request.user, concert=concert, tickets_booked=number_of_tickets)
            return redirect('payments', concert_id=concert.id, number_of_tickets=number_of_tickets)

    return redirect('home')  # Redirect to home if not a POST request

# Cancel ticket view
@login_required
def cancel_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking:
        if (timezone.now() - booking.concert.date_time).total_seconds() < 7200:  # 2 hours
            concert = booking.concert
            concert.available_tickets += booking.tickets_booked
            concert.save()
            booking.delete()
            messages.success(request, 'Your booking has been canceled.')
        else:
            messages.error(request, 'You can only cancel tickets within 2 hours of the concert.')
    return redirect('home')

# Payments view
@login_required
def payments(request, concert_id, number_of_tickets):
    concert = get_object_or_404(Concert, id=concert_id)
    total_price = concert.ticket_price * number_of_tickets

    # Fetch bookings for the user
    bookings = Booking.objects.filter(user=request.user, concert=concert)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        # Here you would handle the payment processing logic
        # For demonstration, we'll assume the payment is always successful
        messages.success(request, "Payment successful! Thank you for your purchase.")
        return redirect('home')  # Redirect to home after payment

    return render(request, 'payments.html', {
        'concert': concert,
        'number_of_tickets': number_of_tickets,
        'total_price': total_price,
        'bookings': bookings,
    })

# Orders view
@login_required
def orders(request):
    bookings = Booking.objects.filter(user=request.user).select_related('concert')
    total_price = sum(booking.tickets_booked * booking.concert.ticket_price for booking in bookings)
    total_tickets = sum(booking.tickets_booked for booking in bookings)

    return render(request, 'orders.html', {
        'bookings': bookings,
        'total_price': total_price,
        'total_tickets': total_tickets,
    })
# Search view
def search(request):
    query = request.GET.get('q', '')
    concerts = Concert.objects.filter(name__icontains=query)  # Example query
    return render(request, 'search_results.html', {'concerts': concerts, 'query': query})

# Cancel booking view
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()  # Delete the booking
    messages.success(request, 'Your booking has been canceled.')
    return HttpResponseRedirect(reverse('orders')) 

# About view
@login_required
def about(request):
    return render(request, 'about.html')  # Render the About Us page

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Concert, Booking
from .forms import ConcertForm

@login_required
def dealer(request):
    concerts = Concert.objects.all()  # Get all concerts
    bookings = Booking.objects.all()  # Get all bookings

    return render(request, 'dealer.html', {
        'concerts': concerts,
        'bookings': bookings,
    })

@login_required
def add_concert(request):
    if request.method == 'POST':
        form = ConcertForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()
            messages.success(request, 'Concert added successfully!')
            return redirect('dealer')  # Redirect to the dealer page after adding
    else:
        form = ConcertForm()

    return render(request, 'add_concert.html', {'form': form})

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Concert
from .forms import ConcertForm

@login_required
def update_concert(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    if request.method == 'POST':
        form = ConcertForm(request.POST, request.FILES, instance=concert)
        if form.is_valid():
            form.save()
            messages.success(request, 'Concert updated successfully!')
            return redirect('dealer')  # Redirect to the dealer page after updating
    else:
        form = ConcertForm(instance=concert)

    return render(request, 'update_concert.html', {'form': form, 'concert': concert})

# views.py
@login_required
def delete_concert(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    if request.method == 'POST':
        concert.delete()
        messages.success(request, 'Concert deleted successfully!')
        return redirect('dealer')  # Redirect to the dealer page after deletion
    return render(request, 'delete_concert.html', {'concert': concert})
# views.py
from django.shortcuts import render
from .models import Concert

def home(request):
    concerts = Concert.objects.all().order_by('date_time')  # Fetch all concerts ordered by date
    return render(request, 'home.html', {'concerts': concerts})
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Concert
from .forms import ConcertForm

@login_required
def add_concert(request):
    if request.method == 'POST':
        form = ConcertForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()  # Save the concert to the database
            messages.success(request, 'Concert added successfully!')
            return redirect('dealer')  # Redirect to the dealer page after adding
    else:
        form = ConcertForm()

    return render(request, 'add_concert.html', {'form': form})

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Concert, Booking

@login_required
def concert_details(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    bookings = Booking.objects.filter(concert=concert)  # Get all bookings for this concert

    return render(request, 'concert_details.html', {
        'concert': concert,
        'bookings': bookings,
    })

# views.py
import qrcode
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Concert, Booking
import io
from PIL import Image, ImageDraw, ImageFont

@login_required
def book_ticket(request):
    if request.method == 'POST':
        concert_id = request.POST.get('concert_id')
        number_of_tickets = int(request.POST.get('number_of_tickets', 0))
        concert = get_object_or_404(Concert, id=concert_id)

        if number_of_tickets > concert.available_tickets:
            messages.error(request, "Not enough tickets available.")
        elif number_of_tickets > 3:
            messages.error(request, "You can only book a maximum of 3 tickets.")
        else:
            concert.available_tickets -= number_of_tickets
            concert.save()
            total_price = concert.ticket_price * number_of_tickets
            booking = Booking.objects.create(user=request.user, concert=concert, tickets_booked=number_of_tickets)

            # Generate QR code with detailed information
            qr_data = (
                f"Concert: {concert.name}\n"
                f"Tickets: {number_of_tickets}\n"
                f"Total: ₹{total_price}\n"
                f"Date: {concert.date_time.strftime('%Y-%m-%d %H:%M')}\n"
                f"Venue: {concert.venue}\n"
                f"Booking ID: {booking.id}"
            )
            qr_image = qrcode.make(qr_data)

            # Create a new blank image for the ticket
            ticket_width = 200
            ticket_height = 350 
            ticket_image = Image.new("RGB", (ticket_width, ticket_height), "white")
            draw = ImageDraw.Draw(ticket_image)

            # Draw the QR code on the ticket image
            qr_image = qr_image.resize((100, 100))  # Resize QR code
            ticket_image.paste(qr_image, (20, 20))  # Position QR code

            # Define the font and size (you may need to adjust the path to a .ttf file)
            font = ImageFont.load_default()  # Use default font
            text = (
                f"Concert: {concert.name}\n"
                f"Tickets: {number_of_tickets}\n"
                f"Total: ₹{total_price}\n"
                f"Date: {concert.date_time.strftime('%Y-%m-%d %H:%M')}\n"
                f"Venue: {concert.venue}\n"
                f"Booking ID: {booking.id}"
            )

            # Draw the text below the QR code
            text_x, text_y = 20, 130  # Position text below the QR code
            draw.text((text_x, text_y), text, fill="black", font=font)

            # Save the ticket image to a BytesIO object
            ticket_io = io.BytesIO()
            ticket_image.save(ticket_io, format='PNG')
            ticket_file = ContentFile(ticket_io.getvalue(), name=f'ticket_{booking.id}.png')

            # Save the ticket image to the booking instance
            booking.qr_code.save(f'ticket_{booking.id}.png', ticket_file)

            return redirect('payments', concert_id=concert.id, number_of_tickets=number_of_tickets)

    return redirect('home')  # Redirect to home if not a POST request

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Concert, Booking

@login_required
def concert_details(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    bookings = Booking.objects.filter(concert=concert)  # Get all bookings for this concert

    return render(request, 'concert_details.html', {
        'concert': concert,
        'bookings': bookings,
    })


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout