from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from eventApp.models import Event, TicketType, Booking
from .serializers import (
    EventSerializer,
    EventCreateSerializer,
    BookingSerializer
)


class CreateEventAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_organizer():
            return Response({"error": "Only organizers can create events"}, status=403)

        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizer=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)



class EditEventAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, event_id):
        event = get_object_or_404(Event, id=event_id, organizer=request.user)

        serializer = EventCreateSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Event updated successfully"})

        return Response(serializer.errors, status=400)


class DeleteEventAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, event_id):
        event = get_object_or_404(Event, id=event_id, organizer=request.user)
        event.delete()
        return Response({"message": "Event deleted"})


class BookEventAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        if request.user.role != "attendee":
            return Response({"error": "Only attendees can book"}, status=403)

        event = get_object_or_404(Event, id=event_id, is_active=True)

        data = {
            "event": event.id,
            "items": request.data.get("items", [])
        }

        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save(attendee=request.user)
            return Response({"message": "Booking successful"}) 

        return Response(serializer.errors, status=400)


class AttendeeBookingsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "attendee":
            return Response({"error": "Only attendees can view bookings"}, status=403)

        bookings = Booking.objects.filter(attendee=request.user, is_active=True)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)



class CancelBookingAPI(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def delete(self, request, booking_id):
        booking = get_object_or_404(
            Booking, id=booking_id, attendee=request.user, is_active=True
        )

        for item in booking.items.all():
            item.ticket_type.quantity += item.quantity
            item.ticket_type.save()

        booking.is_active = False
        booking.save()

        return Response({"message": "Booking cancelled"})
