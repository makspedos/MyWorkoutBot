from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import *
from ..serializer import *


class UserView(APIView):
    def get(self, request, user_email=None, user_password=None, format=None):
        if user_email is None:
            users = User.objects.all()
            user_serializer = UserSerializer(users, many=True)
        else:
            user = User.objects.get(email=user_email,password=user_password)
            user_serializer = UserSerializer(user)
        return Response(user_serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)