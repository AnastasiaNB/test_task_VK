from django.urls import include, path
from rest_framework.routers import SimpleRouter
from friends.views import CustomUserViewSet, FriendsView

router = SimpleRouter()
router.register('users', CustomUserViewSet)

urlpatterns = [
    path(
        'friends/<int:id>/',
        FriendsView.as_view()
    ),
    path('', include(router.urls)),
    path('', include('djoser.urls.authtoken')),
]