from rest_framework import serializers
from eventApp.models import Event, TicketType, Booking, BookingItem
from django.utils import timezone

class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ['id', 'name', 'price', 'quantity']

class EventCreateSerializer(serializers.ModelSerializer):
    ticket_types = TicketTypeSerializer(many=True, read_only=True)  

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'location', 'date', 'ticket_types']



class EventSerializer(serializers.ModelSerializer):
    ticket_types = TicketTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "location",
            "date",
            "is_active",
            "ticket_types"
        ]




class BookingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingItem
        fields = ["ticket_type", "quantity"]


class BookingSerializer(serializers.ModelSerializer):
    items = BookingItemSerializer(many=True)

    class Meta:
        model = Booking
        fields = ["id", "event", "items"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        booking = Booking.objects.create(**validated_data)

        for item in items_data:
            BookingItem.objects.create(booking=booking, **item)

        return booking
