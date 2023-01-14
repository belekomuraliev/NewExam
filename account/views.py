
from rest_framework.generics import ListCreateAPIView
from rest_framework import viewsets
from .models import Author, User
from .serializers import AuthorSerializer


class CreateAuthorAPIView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def perform_create(self, serializer):
        serializer.save(
            registered=self.kwargs.get('registered'),
            user=self.request.user
        )

