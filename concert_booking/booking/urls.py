from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, user_login, book_ticket, cancel_booking, home, search, about, payments, orders  # Import your views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse

from django.urls import path
from .views import register, user_login, book_ticket, cancel_booking, home, search, about, payments, orders, dealer, add_concert  
from django.contrib.auth.views import LogoutView
from .views import dealer, add_concert, update_concert, delete_concert, concert_details, logout_view  # Ensure all views are imported, 

urlpatterns = [
    path('signup/', register, name='signup'),
    path('login/', user_login, name='login'),
    path('book_ticket/', book_ticket, name='book_ticket'),
    path('cancel_booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('about/', about, name='about'),
    path('payments/<int:concert_id>/<int:number_of_tickets>/', payments, name='payments'),
    path('orders/', orders, name='orders'),
    path('logout/', logout_view, name='logout'),
    path('dealer/', dealer, name='dealer'),  # Dealer page
    path('dealer/add/', add_concert, name='add_concert'),  # Add concert page
    path('concert/update/<int:concert_id>/', update_concert, name='update_concert'),  # Update concert
    path('concert/delete/<int:concert_id>/', delete_concert, name='delete_concert'),  # Delete concert
    path('concert/details/<int:concert_id>/', concert_details, name='concert_details'),  # Concert details
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

