from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializer import *


def func(request):
    return render(request, 'html/home.html')


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

class WorkoutView(APIView):
    def get(self, request, program_id=None):
        if program_id is None:
            workouts = Workout.objects.all()
        else:
            workouts = Workout.objects.filter(programs=program_id)
            if not len(workouts):
                return Response(False)

        workout_serializer = WorkoutSerializer(workouts, many=True)
        return Response(workout_serializer.data)

    def post(self, request, format=None):
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)



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

class ExerciseProgramView(APIView):
    def get(self, request, workout_id, format=None):
        exercises = Exercise.objects.filter(workout=workout_id).distinct()
        exercises_serializer = ExerciseSerializer(exercises, many=True)
        return Response(exercises_serializer.data)

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


class MuscleView(APIView):
    def get(self, request, muscle_id=None, format=None):
        if muscle_id is None:
            muscles = Muscle.objects.all()
            muscle_serializer = MuscleSerializer(muscles, many=True)
        else:
            muscle = Muscle.objects.get(id=muscle_id)
            muscle_serializer = MuscleSerializer(muscle)
        return Response(muscle_serializer.data)


class LoadView(APIView):
    def get(self, request, exercise_id=None, workout_id=None, format=None):
        if exercise_id is None:
            loads = Load.objects.all()
        else:
            loads = Load.objects.filter(exercise=exercise_id, workout_id=workout_id)
        loads_serializer = LoadSerializer(loads, many=True)
        return Response(loads_serializer.data)

    def post(self, request, format=None):
        serializer = LoadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
