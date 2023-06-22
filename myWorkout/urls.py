from django.urls import path
from . import views

urlpatterns = [
    path('program/', views.ProgramView.as_view()),
    path('program/<int:user_id>/', views.ProgramView.as_view()),

    path('program/<int:program_id>/exercise/workout/', views.WorkoutView.as_view()),
    path('program/workout/', views.WorkoutView.as_view()),

    path('program/exercise/muscle/<int:muscle_id>/', views.MuscleExerciseView.as_view()),
    path('program/exercise/<int:exercise_id>/', views.ExerciseView.as_view()),
    path('program/exercise/workout/<int:workout_id>/', views.ExerciseProgramView.as_view()),


    path('program/user/<str:user_email>/<str:user_password>/', views.UserView.as_view()),
    path('program/user/', views.UserView.as_view()),

    path('program/muscle/<int:muscle_id>/', views.MuscleView.as_view()),
    path('program/muscle/', views.MuscleView.as_view()),


    path('program/load/<int:exercise_id>/<int:workout_id>/', views.LoadView.as_view()),
    path('program/load/', views.LoadView.as_view()),
]

