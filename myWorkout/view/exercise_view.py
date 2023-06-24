from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import *
from ..serializer import *

class ExerciseView(APIView):
    def get(self, request, exercise_id, format=None):
        exercises = Exercise.objects.filter(id=exercise_id)
        exercises_serializer = ExerciseSerializer(exercises, many=True)
        return Response(exercises_serializer.data)

    def patch(self, request, exercise_id, format=None):
        exercise = Exercise.objects.get(id=exercise_id)
        workout_id = request.data.get('workout')
        workout = Workout.objects.get(id=workout_id)
        exercise.workout.add(workout)
        serializer = ExerciseSerializer(exercise)
        return Response(serializer.data)


class MuscleExerciseView(APIView):
    def get(self, request, muscle_id, format=None):
        exercises = Exercise.objects.filter(muscle=muscle_id)
        exercises_serializer = ExerciseSerializer(exercises, many=True)
        return Response(exercises_serializer.data)


class ExerciseWorkoutView(APIView):
    def get(self, request, workout_id, format=None):
        exercises = Exercise.objects.filter(workout=workout_id).distinct()
        exercises_serializer = ExerciseSerializer(exercises, many=True)
        return Response(exercises_serializer.data)

class ExerciseProgramView(APIView):
    def get(self, request, program_id, format=None):
        exercises = Exercise.objects.filter(workout__programs=program_id).distinct()
        exercises_serializer = ExerciseSerializer(exercises, many=True)
        return Response(exercises_serializer.data)