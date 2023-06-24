from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import *
from ..serializer import *


class LoadView(APIView):
    def get(self, request, exercise_id=None, workout_id=None, program_id=None, format=None):
        if exercise_id is None:
            loads = Load.objects.all()
        else:
            loads = Load.objects.filter(exercise=exercise_id, workout_id=workout_id, program_id=program_id)
        loads_serializer = LoadSerializer(loads, many=True)
        return Response(loads_serializer.data)

    def post(self, request, format=None):
        serializer = LoadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

class LoadProgramView(APIView):
    def get(self, request, exercise_id=None, program_id=None, format=None):
        if exercise_id is None:
            loads = Load.objects.all()
        else:
            loads = Load.objects.filter(exercise=exercise_id, program_id=program_id)
        loads_serializer = LoadSerializer(loads, many=True)
        return Response(loads_serializer.data)