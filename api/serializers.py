from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
	"""UserSerializer"""
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
		write_only_fields = ('password',)