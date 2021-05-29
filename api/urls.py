from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import PostViewSet, CommentViewSet, FollowViewSet, GroupViewSet

router_v1 = DefaultRouter()
router_v1.register('v1/posts', PostViewSet, basename='PostView')
router_v1.register(
    r'v1/posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='CommentView'
)
router_v1.register('v1/follow', FollowViewSet, basename='FollowView')
router_v1.register('v1/group', GroupViewSet, basename='GroupView')

urlpatterns = [
    path('', include(router_v1.urls)),
    path(
        'v1/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

]
