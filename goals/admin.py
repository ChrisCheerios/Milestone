from django.contrib import admin
from .models import *
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter

# Register your models here.


# The Admin Class for Goal_Progress
class Goal_Progress_Admin(admin.ModelAdmin):
    def username(self,obj):
        return (f"{obj.goal.user}")

    # Modifies what information is displayed, and how it can be filtered in the admin view
    list_display = ['__str__','quantity','username','goal']
    list_filter = ['goal']


# The 'parent' admin class for the different types of goals.  Required for polymorphic models
class GoalChildAdmin(PolymorphicChildModelAdmin):
    base_model = Goal

# The admin class for the goal archetype
@admin.register(Goal)
class GoalParentAdmin(PolymorphicParentModelAdmin):
    base_model = Goal
    # child_models = (Cumulative_Goal, Milestone_Goal) Commenting out this line as Milestone Goals are being scrapped from final version
    child_models = [Cumulative_Goal]
    list_filter = (PolymorphicChildModelFilter,)

# The extension for the cumulative goal admin model
@admin.register(Cumulative_Goal)
class Cumulative_GoalAdmin(GoalChildAdmin):
    base_model = Cumulative_Goal

# # The extension for the  goal admin model
# @admin.register(Milestone_Goal)
# class Milestone_Goal(GoalChildAdmin):
#     base_model = Milestone_Goal

admin.site.register(Goal_Progress, Goal_Progress_Admin)
