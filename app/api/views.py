from rest_framework import permissions
from ..models import Customer
from .serializers import CustomerSerializer
from rest_framework.generics import ListAPIView,CreateAPIView,ListCreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated   


class CustomerListCreate(ListCreateAPIView):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    authentication_classes=[BasicAuthentication]
   # permission_classes=[IsAuthenticatedOrReadOnly]
    permission_classes=[IsAuthenticated]



    