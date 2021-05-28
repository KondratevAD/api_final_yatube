from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import PostViewSet, CommentViewSet, FollowViewSet, GroupViewSet

router_v1 = DefaultRouter()
router_v1.register('posts', PostViewSet, basename='PostView')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='CommentView'
)
router_v1.register('follow', FollowViewSet, basename='FollowView')
router_v1.register('group', GroupViewSet, basename='GroupView')

urlpatterns = [
    path('', include(router_v1.urls)),
    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

]
