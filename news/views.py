from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import News, Comment, Status, CommentStatus, NewsStatus, Count
from .serializers import NewsSerializer, CommentSrializer, StatusSrializer
from .permissions import IsOwnerPermission


class NewsCreateListAPIView(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['title',]
    ordering_fields = ['created']

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            news=self.kwargs.get('news_id'),
        )


class NewsUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        return get_object_or_404(News, pk=self.kwargs.get('news_id'))


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSrializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerPermission]

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
        )


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSrializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerPermission]


class StatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSrializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class StatusRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSrializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        return get_object_or_404(Status, pk=self.kwargs.get('slug'))



