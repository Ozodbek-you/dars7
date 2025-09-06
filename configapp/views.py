from django.shortcuts import render




from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from .make_token import get_tokens_for_user
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics, permissions
from .models import ToDoList, User
from .serializers import ToDoListSerializer, UserCreateSerializer
class LoginUser(APIView):
    @swagger_auto_schema(request_body=LoginSerializers)
    def post(self,request):
        serializer = LoginSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User,username = serializer.validated_data.get('username'))
        token = get_tokens_for_user(user)
        return Response(data=token)



class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAdmin]


class ToDoListViewSet(viewsets.ModelViewSet):
    serializer_class = ToDoListSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return ToDoList.objects.all()
        elif self.request.user.is_user:
            return ToDoList.objects.filter(user=self.request.user,bajarilgan= False)

    def perform_create(self, serializer):
        if self.request.user.is_admin:
            serializer.save(bajarilgan = False)
        else:
            raise PermissionDenied("Sizga task yaratishga ruxsat yo‘q")

class UserListView(generics.ListAPIView):
    queryset = User.objects.filter(is_user=True)
    serializer_class = UserCreateSerializer
    permission_classes = [IsAdmin]

















































