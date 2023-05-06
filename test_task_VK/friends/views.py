from djoser.views import UserViewSet
from rest_framework import permissions, status, views
from rest_framework.decorators import action
from rest_framework.response import Response

from friends.models import FriendRequest, Status, User
from friends.serializers import FriendRequestSerializer


class CustomUserViewSet(UserViewSet):
    @action(["get"], detail=False)
    def my_friends(self, request, *args, **kwargs):
        friendrequests = FriendRequest.objects.filter(
            user_from=request.user,
            status=Status.objects.get(id=2)
        )
        friends = [friendrequest.user_to for friendrequest in friendrequests]
        data = [self.get_serializer(friend).data for friend in friends]
        return Response(data=data, status=status.HTTP_200_OK)

    @action(["get"], detail=False)
    def my_followers(self, request, *args, **kwargs):
        friendrequests = FriendRequest.objects.filter(
            user_to=request.user,
            status=Status.objects.get(id=1)
        )
        friends = [friendrequest.user_from for friendrequest in friendrequests]
        data = [self.get_serializer(friend).data for friend in friends]
        return Response(data=data, status=status.HTTP_200_OK)

    @action(["get"], detail=False)
    def i_follow(self, request, *args, **kwargs):
        friendrequests = FriendRequest.objects.filter(
            user_from=request.user,
            status=Status.objects.get(id=1)
        )
        friends = [friendrequest.user_to for friendrequest in friendrequests]
        data = [self.get_serializer(friend).data for friend in friends]
        return Response(data=data, status=status.HTTP_200_OK)

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
        if request.user.id == kwargs['id']:
            return Response(
                data={
                    'message': 'You can not send friend request to yourself'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        data = {
            'user_from': request.user.id,
            'user_to': kwargs['id'],
        }
        user_to = User.objects.get(id=kwargs['id'])
        try:
            request_to = FriendRequest.objects.get(
                user_to=request.user,
                user_from=user_to
            )
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

    def delete(self, request, *args, **kwargs):
        user_to = User.objects.get(id=kwargs['id'])
        try:
            FriendRequest.objects.get(
                user_from=request.user,
                user_to=user_to
            ).delete()
        except FriendRequest.DoesNotExist:
            return Response(
                data={'message': 'Object matching query does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            friend_request = FriendRequest.objects.get(
               user_to=request.user,
               user_from=user_to
            )
            friend_request.status = Status.objects.get(id=1)
            friend_request.save()
        except FriendRequest.DoesNotExist:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
