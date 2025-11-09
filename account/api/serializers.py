

from rest_framework import serializers
from django.contrib.auth import get_user_model
from eventApp.models import Event

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'role', 'phone', 'address')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','role','phone','address')


class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ('id','organizer','title','description','location','date','is_active','created_at','updated_at')
