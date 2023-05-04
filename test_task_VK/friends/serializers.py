from rest_framework import serializers
from friends.models import FriendRequest

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('user_from', 'user_to', 'status')