from django.db import models
from django.conf import settings


TICKET_TYPE_CHOICES = (
    ("early_bird", "Early Bird"),
    ("regular", "Regular"),
    ("vip", "VIP"),
)

class Event(models.Model):
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organized_events"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  

    def __str__(self):
        return self.title


class TicketType(models.Model):
  
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="ticket_types")
    name = models.CharField(max_length=50, choices=TICKET_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()  

    def __str__(self):
        return f"{self.event.title} - {self.name}"


class Booking(models.Model):
    """
    Represents a ticket booking by an attendee
    """
    attendee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="bookings")
    booked_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.attendee.username} - {self.event.title}"


class BookingItem(models.Model):
    """
    Represents tickets booked for a specific ticket type
    """
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="items")
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.booking.attendee.username} - {self.ticket_type.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        """
        Override save to update ticket inventory dynamically
        """
        if not self.pk:  
            if self.ticket_type.quantity < self.quantity:
                raise ValueError(
                    f"Not enough tickets available for {self.ticket_type.name}"
                )
            self.ticket_type.quantity -= self.quantity
            self.ticket_type.save()
        super().save(*args, **kwargs)
