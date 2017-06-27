# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from api.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics


class UserList(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
		