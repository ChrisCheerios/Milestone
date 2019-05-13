from django.db import models
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel


class Goal(PolymorphicModel):

    # Every goal is associated with a title and a user
    title = models.CharField(max_length=40)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="1")

    # Target Completion Date
    target_date = models.DateField(default="2019-04-22")

    # Setting the options for the size of the goal

    SMALL = 's'
    MEDIUM = 'm'
    LARGE = 'l'

    GOAL_SIZE_CHOICES = (
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large')
    )

    goal_size = models.CharField(
        max_length=10,
        choices=GOAL_SIZE_CHOICES,
        default=SMALL
    )

    # Sets whether the goal with be visible to other users
    private = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"


# The model for cumulative goals with incremental progress - like doing 10,000 pushups
class Cumulative_Goal(Goal):

    # A boolean to mark completion
    complete = models.BooleanField(default=False)

    # Set the goal amount and the unit (ie. 10,00 pushups)
    units = models.CharField(max_length=40)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    # Set the Users preferred pace of completion
    # chunk-size is how many they need to do per period (eg 400 pushups per week)
    chunk_size = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}"

# # The model for 'milestone' goals - like running a marathon - for which progress
# # is not discretely quantifiablw.
# class Milestone_Goal(Goal):
#
#     # The final goal
#     final_goal=models.CharField(max_length=150, default="")
#     # A boolean to mark completion
#     complete = models.BooleanField(default=False)
#
# class Milestone_Step(models.Model):
#
#     # Intermediate steps for milestones each with a name and a completion boolean
#     goal = models.ForeignKey(Milestone_Goal, on_delete=models.CASCADE, related_name='steps')
#     step_one = models.CharField(max_length=150, null=True)
#     step_one_complete =  models.BooleanField(default=False)
#


# Progress for goals
class Goal_Progress(models.Model):

    # Link the progress to the goal
    goal = models.ForeignKey(
        Cumulative_Goal,
        on_delete=models.CASCADE,
        related_name="progress"
    )

    # Quantity of the unit logged
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    # Timestamp
    timestamp = models.DateField()

    def __str__(self):
        return f"{self.quantity} {self.goal.units} at {self.timestamp}"
