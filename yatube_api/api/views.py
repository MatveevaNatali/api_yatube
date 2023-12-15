from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets

from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post

API_403 = PermissionDenied('Запрет на внесение изменений')


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_post_method(self):
        post_new = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post_new

    def get_queryset(self):
        post = self.get_post_method()
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post = self.get_post_method()
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise API_403
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise API_403
        instance.delete()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise API_403
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise API_403
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
