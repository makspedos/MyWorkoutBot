from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import *
from ..serializer import *


class ProgramView(APIView):
    def get(self, request, user_id=None):
        if user_id is None:
            all_programs = Program.objects.all()
            program_serializer = ProgramSerializer(all_programs, many=True)
        else:
            program = Program.objects.get(user=user_id)
            program_serializer = ProgramSerializer(program)
        return Response(program_serializer.data)

    def post(self, request, format=None):
        serializer = ProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)