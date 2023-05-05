from rest_framework import serializers
from djoser.serializers import UserSerializer
from friends.models import FriendRequest, User


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('user_from', 'user_to', 'status')


class CustomUserSerializer(UserSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'status')

    def get_status(self, instance):
        try:
            friend_request = FriendRequest.objects.get(
                user_from=self.context.get('request').user,
                user_to=instance
            )
            if friend_request.status.id == 1:
                return 'I follow'
            return friend_request.status.status
        except FriendRequest.DoesNotExist:
            try:
                friend_request = FriendRequest.objects.get(
                    user_to=self.context.get('request').user,
                    user_from=instance
                )
                return 'My follower'
            except FriendRequest.DoesNotExist:
                return ''
