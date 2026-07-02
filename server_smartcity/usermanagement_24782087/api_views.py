from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from .serializers import RegisterSerializer

User = get_user_model()


@extend_schema(exclude=True)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
