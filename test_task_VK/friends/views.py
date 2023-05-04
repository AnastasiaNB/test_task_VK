from djoser.views import UserViewSet
from rest_framework import views
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.response import Response
from friends.serializers import FriendRequestSerializer
from friends.models import FriendRequest, Status


class CustomUserViewSet(UserViewSet):
    def activation(self, request, *args, **kwargs):
        pass

    def resend_activation(self, request, *args, **kwargs):
        pass

    def set_password(self, request, *args, **kwargs):
        pass

    def reset_password(self, request, *args, **kwargs):
        pass

    def reset_password_confirm(self, request, *args, **kwargs):
        pass

    def set_username(self, request, *args, **kwargs):
        pass

    def reset_username(self, request, *args, **kwargs):
        pass

    def reset_username_confirm(self, request, *args, **kwargs):
        pass


class FriendsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = {
            'user_from': request.user.id,
            'user_to': kwargs['id'],
        }
        try:
            request_to = FriendRequest.objects.get(user_to=request.user)
            request_to.status = Status.objects.get(id=2)
            request_to.save()
            data['status'] = 2
        except FriendRequest.DoesNotExist:
            data['status'] = 1
        serializer = FriendRequestSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
