from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import News, Comment, Status, CommentStatus, NewsStatus
from .serializers import NewsSerializer, CommentSrializer, StatusSrializer, NewsStatusSrializer, CommentStatusSrializer
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

    def get_object(self):
        return get_object_or_404(Comment, pk=self.kwargs.get('comment_id'))


class StatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSrializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class StatusRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSrializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class NewsStatusAPIV(APIView):
    def get_object(self):
        return get_object_or_404(NewsStatus, pk=self.kwargs.get('slug'))

    def get(self, request, *args, **kwargs):
        items = NewsStatus.objects.all()
        serializer = NewsStatusSrializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = NewsStatusSrializer(self.get_object())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, "Status added")
        else:
            return Response(serializer.errors, "You already added status")


class CommentStatusAPIV(APIView):
    def get_object(self):
        return get_object_or_404(CommentStatus, pk=self.kwargs.get('slug'))

    def get(self, request, *args, **kwargs):
        comment = CommentStatus.objects.all()
        serializer = CommentStatusSrializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CommentStatusSrializer(self.get_object())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, "Status added")
        else:
            return Response(serializer.errors, "You already added status")
