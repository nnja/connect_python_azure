from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from tweeter.models import Tweet, User
from tweeter.permissions import IsAuthorOrReadOnly, IsSelfOrAdmin
from tweeter.serializers import TweetSerializer, UserSerializer

from django.contrib.auth import authenticate, login


def index(request):
    # As an example, let's always log in as the user Bob.
    bob = User.objects.get(first_name='Bob')
    login(request, bob)

    return render(request, 'tweeter/index.html')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSelfOrAdmin]


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
