from django.urls import path

from .view import exercise_view, load_view, muscle_view, program_view, user_view, workout_view


urlpatterns = [
    path('program/', program_view.ProgramView.as_view(), name='programs'),
    path('program/user/<int:user_id>/', program_view.ProgramView.as_view(), name='programs_by_user'),

    path('workout/program/<int:program_id>/', workout_view.WorkoutView.as_view()),
    path('workout/', workout_view.WorkoutView.as_view()),
    path('workout/<int:program_id>/', workout_view.WorkoutView.as_view()),
    path('workout/program/<int:program_id>/<str:workout_name>/', workout_view.WorkoutProgramView.as_view()),

    path('exercise/muscle/<int:muscle_id>/', exercise_view.MuscleExerciseView.as_view()),
    path('exercise/<int:exercise_id>/', exercise_view.ExerciseView.as_view()),
    path('exercise/workout/<int:workout_id>/', exercise_view.ExerciseWorkoutView.as_view()),
    path('exercise/program/<int:program_id>/', exercise_view.ExerciseProgramView.as_view()),

    path('user/data/<str:user_email>/<str:user_password>/', user_view.UserView.as_view()),
    path('user/', user_view.UserView.as_view()),

    path('muscle/<int:muscle_id>/', muscle_view.MuscleView.as_view()),
    path('muscle/', muscle_view.MuscleView.as_view()),


    path('load/exercise/workout/program/<int:exercise_id>/<int:workout_id>/<int:program_id>/', load_view.LoadView.as_view()),
    path('load/exercise/program/<int:exercise_id>/<int:program_id>/', load_view.LoadProgramView.as_view()),
    path('load/', load_view.LoadView.as_view()),
]

