from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from .models import *
import csv
from .forms import UploadFileForm

# Registration View, adapted from https://overiq.com/django-1-10/django-creating-users-using-usercreationform/
def register(request):
    if request.method == 'POST':
        user = UserCreationForm(request.POST)
        if user.is_valid():
            user.save()
            return HttpResponseRedirect(reverse("login"))
        else:
            context = {
                "form": UserCreationForm(),
                "message": "Registration Failed"
            }
            return render(request, 'registration/register.html', context)
    else:
        context = {
            "form": UserCreationForm()
        }
        return render(request, 'registration/register.html', context)

# Logout Users and redirect to the login
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

# Log in Users
def login_view(request):

    # On GET we render the login page
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "registration/login.html")

    # On POST we authenticate and login the user
    else:
        try:
            username = request.POST["username"]
            password = request.POST["password"]
        except:
            context = {"message": "Error with Credentials"}
            return render(request, "registration/login.html", context)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            context = {"message": "Error with Credentials"}
            return render(request, "registration/login.html", context)



def index(request):
    # Check if the user is authenticated.  If not - return to login screen
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    # Grab the user's goals
    goals = Goal.objects.filter(user = request.user)

    # Grab any progress associated with the user's goals:
    progress = {}

    for goal in goals:
        progress[goal] = list(
            Goal_Progress.objects.filter(goal = goal).order_by('timestamp').reverse())

    # Pass the user and their goals
    context = {
        "user": request.user,
        "progress": progress,
        "goals": goals
    }

    return render(request, "goals/home.html", context)

@login_required
def add_goal(request):
    if request.method == "GET":
        # Pass the user to the template
        context = {
            "user": request.user,
        }
        return render(request, "goals/new_goal.html", context)

    # On POST we are submitting a new goal and need to update the db.
    else:
        # Check if it is a journey  goal
        if request.POST["goal_type"] == "journey":
            # Grab the data from the form
            title = request.POST["journey-title"]
            units = request.POST["journey-unit"]
            total = request.POST["journey-quantity"]
            chunk_size = request.POST["journey-chunk-size"]
            period = request.POST["journey-period"]

            # Mark the privacy status of the goal
            if 'journey-private' in request.POST:
                private = request.POST['journey-private']
            else:
                private = False

            cumulative_goal = Cumulative_Goal(title=title, user=request.user,
                units=units, total=total, chunk_size=chunk_size, period=period)
            cumulative_goal.save()
        # If it is a milestone goal, process this way
        else:
            pass

        # Route the user home!
        return HttpResponseRedirect(reverse("index"))


def view_goal (request, id):
    if request.method == "GET":

        # Check that the goal exists and belongs to the user:
        goal = Cumulative_Goal.objects.get(pk=id)

        if goal.user != request.user:
            return HttpResponseRedirect(reverse("index"))

        # Grab any progress associated with the goal
        progress = goal.progress.all().order_by('timestamp').reverse()

        # The csv file form:
        form = UploadFileForm()

        context = {
            "goal": goal,
            "progress": progress,
            'form': form
        }

        return render(request, "goals/goal_view.html", context)

    # On Post - We are logging progress that the user has submitted
    else:

        # Grab the data from the form:
        #pq=progress-quanity, pd=progress-date
        pq_one = request.POST["progress-quantity-1"]
        pd_one = request.POST["progress-date-1"]

        pq_two = request.POST["progress-quantity-2"]
        pd_two = request.POST["progress-date-2"]

        pq_three = request.POST["progress-quantity-3"]
        pd_three = request.POST["progress-date-3"]

        #Retrieve the goal associated with the progress
        goal_id = request.POST["goal"]
        goal=Cumulative_Goal.objects.get(pk=goal_id)

        # Create Goal_progress instances for each of the recorded progresses
        progress = Goal_Progress(goal=goal, quantity=pq_one, timestamp=pd_one)
        progress.save()

        #If the user submitted multiple progress logs, we update those as well
        if pq_two and pd_two:
            progress = Goal_Progress(goal=goal, quantity=pq_two, timestamp=pd_two)
            progress.save()
        if pq_three and pd_three:
            progress = Goal_Progress(goal=goal, quantity=pq_three, timestamp=pd_three)
            progress.save()

        # Return the user to the goal page
        return HttpResponseRedirect(reverse("view_goal", args=[goal.id]))

# My View to retrieve the goal-data for the progress chart
class goal_progress_data(APIView):

    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    authentication_classes = []
    permission_classes = []

    # On get, this API call should return the list of progress for the provided goal
    def get(self, request, id, format=None):

        # Retrieve the list of progress-updates for the given goal
        progress = [log.quantity for log in Goal_Progress.objects.filter(goal=id).order_by('timestamp')]

        # Calculate a list of the cumulative progress at each update, which is also used for the data visualization
        cumulative_progress = []
        for quantity in progress:
            cumulative_progress.append(quantity)
            if  len(cumulative_progress) >= 2:
                cumulative_progress[-1] = cumulative_progress[-1] + cumulative_progress[-2]

        # List of the Dates for the progress updates
        dates = [log.timestamp for log in Goal_Progress.objects.filter(goal=id).order_by('timestamp')]

        # Package the data
        data ={
            "progress" : progress,
            "cumulative_progress": cumulative_progress,
            "dates" : dates
        }

        # Return the data
        return Response(data)

    # On Post we are updating the progress-log data
    def post(self, request, id, format=None):


        #Retrieve the relevant goal
        goal_progress = Goal_Progress.objects.get(pk=request.data["progress_id"])
        goal_progress.quantity = request.data["quantity_edit"]
        goal_progress.timestamp = request.data["date_edit"]


        # If the quantity is set to 0- we delete the progresses
        if goal_progress.quantity == "0":
            goal_progress.delete()
        else:
            goal_progress.save()

        return Response(status=status.HTTP_201_CREATED)


def read_csv(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))
    else:
        # fetch the associated goal:
        goal = Cumulative_Goal.objects.get(pk=request.POST["goal"])

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file'].chunks()

            with open('goals/temp.txt', 'wb+') as destination:
                for chunk in file:
                    destination.write(chunk)

            with open('goals/temp.txt') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for date, quantity in reader:
                    try:
                        progress = Goal_Progress(quantity = quantity, timestamp=date, goal=goal)
                        progress.save()
                    except:
                        pass
        return HttpResponseRedirect(reverse('index'))
