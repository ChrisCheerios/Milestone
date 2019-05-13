from django.urls import path, re_path
from . import views
from .views import goal_progress_data

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('addgoal', views.add_goal, name='add_goal'),
    path('logout/', views.logout_view, name='log_out'),
    path('login/', views.login_view, name="login"),
    path('viewgoal/<int:id>/', views.view_goal, name='view_goal'),
    path('api/data/<int:id>', goal_progress_data.as_view()),
    path('viewgoal/form', views.read_csv, name="csv")
]
