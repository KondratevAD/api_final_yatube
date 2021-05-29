from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins
from rest_framework.exceptions import ParseError
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .models import Comment, Follow, Group, Post, User
from .permissions import IsContentAuthor
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsContentAuthor]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsContentAuthor]

    def list(self, request, post_id):
        comments = Comment.objects.filter(post=post_id).all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(
            author=self.request.user,
            post_id=post.id
        )


class GetPostViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    pass


class FollowViewSet(GetPostViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['following__username', 'user__username', ]

    def perform_create(self, serializer):
        if self.request.data:
            author = self.request.data['following']
        elif self.request.query_params:
            author = self.request.query_params['user']
        else:
            author = self.request.user.username
        following = get_object_or_404(User, username=author)
        follower = self.request.user.follower.values().filter(
            following_id=following.id
        ).exists()
        if author == self.request.user.username:
            raise ParseError(detail="you can't subscribe to yourself")
        elif follower is True:
            raise ParseError(detail='already subscribed to this user')
        else:
            serializer.save(user=self.request.user, following=following)

    def filter_queryset(self, queryset):
        if self.request.data:
            following = get_object_or_404(
                User,
                username=self.request.data['user']
            )
        else:
            following = get_object_or_404(User, username=self.request.user)
        queryset = self.queryset.filter(following=following).all()
        filter_backends = [filters.SearchFilter]
        for backend in list(filter_backends):
            queryset = backend().filter_queryset(
                self.request,
                queryset,
                view=self
            )
        return queryset


class GroupViewSet(GetPostViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsContentAuthor]

    def perform_create(self, serializer):
        serializer.save(title=self.request.data['title'])
