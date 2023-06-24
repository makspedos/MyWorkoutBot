from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import *
from ..serializer import *


class WorkoutView(APIView):
    def get(self, request, program_id=None):
        if program_id:
            workouts = Workout.objects.filter(programs=program_id)
            if not len(workouts):
                return Response(False)
        else:
            workouts = Workout.objects.all()
        workout_serializer = WorkoutSerializer(workouts, many=True)
        return Response(workout_serializer.data)

    def post(self, request, format=None):
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    def delete(self, request, workout_name, program_id):
        workout = Workout.objects.get(name=workout_name, programs=program_id)
        workout.delete()
        return Response('Deleted')

class WorkoutProgramView(APIView):
    def get(self, request, program_id=None, workout_name=None):
        if program_id and workout_name:
            workouts = Workout.objects.filter(name=workout_name, programs=program_id)
        else:
            workouts = Workout.objects.all()
        workout_serializer = WorkoutSerializer(workouts, many=True)
        return Response(workout_serializer.data)

    def delete(self, request, workout_name, program_id):
        workout = Workout.objects.get(name=workout_name, programs=program_id)
        workout.delete()
        return Response('Deleted')