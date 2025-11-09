from django.contrib import admin
from eventApp.models import Event, Booking, BookingItem, TicketType

# Register your models here.

admin.site.register(Event)
admin.site.register(Booking)
admin.site.register(BookingItem)
admin.site.register(TicketType)

