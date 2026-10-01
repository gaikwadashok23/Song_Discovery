from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer


class UserCreateView(APIView):

    def post(self, request):

        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        if User.objects.filter(email=email).exists():
            return Response(
                {
                    "error": "User with this email already exists."
                },
                status=status.HTTP_409_CONFLICT,
            )

        user = serializer.save()

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class UserDetailView(APIView):

    def get(self, request, user_id):

        user = get_object_or_404(
            User,
            id=user_id,
        )

        serializer = UserSerializer(user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )