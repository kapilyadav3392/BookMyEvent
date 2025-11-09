from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Event, Booking, TicketType, BookingItem
from django.contrib import messages
from django.db import transaction
from django.utils import timezone

@login_required
def create_event(request):
    if not request.user.is_organizer():
        return redirect("home")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        location = request.POST.get("location")
        date = request.POST.get("date")

        if not (title and description and location and date):
            return render(request, "create_event.html", {"error": "All fields are required."})

        event = Event.objects.create(
            organizer=request.user,
            title=title,
            description=description,
            location=location,
            date=date,
            is_active = True
        )

        
        i = 0
        while True:
            ticket_name = request.POST.get(f"ticket_name_{i}")
            ticket_price = request.POST.get(f"ticket_price_{i}")
            ticket_quantity = request.POST.get(f"ticket_quantity_{i}")
            if not ticket_name:  # Stop when no more fields
                break
            event.ticket_types.create(
                name=ticket_name,
                price=ticket_price,
                quantity=ticket_quantity
            )
            i += 1

        return redirect("account:event_manage")

    return render(request, "createEvent.html")




@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)

    
    editing_locked = event.date < timezone.now()

    ticket_types = TicketType.objects.filter(event=event)

    if request.method == "POST" and not editing_locked:

        
        event.title = request.POST.get("title")
        event.description = request.POST.get("description")
        event.location = request.POST.get("location")
        event.date = request.POST.get("date")
        event.save()

        
        delete_ids = request.POST.getlist("delete_ticket_type")
        if delete_ids:
            TicketType.objects.filter(id__in=delete_ids, event=event).delete()

        
        for t in ticket_types:
            t.name = request.POST.get(f"name_{t.id}")
            t.price = request.POST.get(f"price_{t.id}")
            t.quantity = request.POST.get(f"quantity_{t.id}")
            t.save()

        
        new_name = request.POST.get("new_name")
        new_price = request.POST.get("new_price")
        new_quantity = request.POST.get("new_quantity")

        if new_name and new_price and new_quantity:
            TicketType.objects.create(
                event=event,
                name=new_name,
                price=new_price,
                quantity=new_quantity
            )

        return redirect("account:event_manage")

    context = {
        "event": event,
        "ticket_types": ticket_types,
        "editing_locked": editing_locked,
    }
    return render(request, "edit_event.html", context)

@login_required
def cancel_event(request, event_id):
    event = Event.objects.get(id=event_id, organizer=request.user)
    event.delete()
    return redirect("account:event_manage")


@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, is_active=True)
    ticket_types = TicketType.objects.filter(event=event)

    if request.user.role != "attendee":
        messages.error(request, "Only attendees can book tickets.")
        return redirect("event_manage")  

    if request.method == "POST":
        
        booking = Booking.objects.create(
            attendee=request.user,
            event=event
        )

        
        for ttype in ticket_types:
            qty = int(request.POST.get(f"ticket_{ttype.id}", 0))

            if qty > 0:
               
                BookingItem.objects.create(
                    booking=booking,
                    ticket_type=ttype,
                    quantity=qty
                )

        messages.success(request, "Tickets booked successfully!")
        return redirect("attendee_bookings")  

    return render(request, "book_event.html", {
        "event": event,
        "ticket_types": ticket_types
    })


@login_required
def attendee_bookings(request):
    if request.user.role != "attendee":
        messages.error(request, "Only attendees can view bookings.")
        return redirect("home")

    bookings = Booking.objects.filter(attendee=request.user, is_active=True)

    return render(request, "attendee_bookings.html", {
        "bookings": bookings
    })

@login_required
@transaction.atomic
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        attendee=request.user,
        is_active=True
    )

    
    for item in booking.items.all():
        item.ticket_type.quantity += item.quantity
        item.ticket_type.save()

    booking.is_active = False
    booking.save()

    messages.success(request, "Your booking has been cancelled successfully.")
    return redirect("attendee_bookings")


@login_required
def delete_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return HttpResponse("Invalid booking", status=404)

    
    if booking.event.organizer != request.user:
        return HttpResponse("Not allowed", status=403)

    event_id = booking.event.id

    
    for item in booking.items.all():
        ticket = item.ticket_type
        ticket.quantity += item.quantity
        ticket.save()

    booking.delete()

    return redirect("account:event_manage")