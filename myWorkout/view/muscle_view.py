from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import *
from ..serializer import *



class MuscleView(APIView):
    def get(self, request, muscle_id=None, format=None):
        if muscle_id is None:
            muscles = Muscle.objects.all()
            muscle_serializer = MuscleSerializer(muscles, many=True)
        else:
            muscle = Muscle.objects.get(id=muscle_id)
            muscle_serializer = MuscleSerializer(muscle)
        return Response(muscle_serializer.data)