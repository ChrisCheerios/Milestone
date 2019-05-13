# MileStone Final Project CS33
## Chris Sorenson, 05/13/2019

## Intro:
* This is a goal tracking web-app.  I did not nearly manage to implement all of the features I dreamed about!  I've left some of the remnants of my incomplete efforts in the files (commented out) so that I can return later to work further.
* The big feature cut was I removed the titular Milestone Goals from the project, as I was not able to get the features on MileStones to the same level as my Journey-type Goals.  
* My plan was to make a goals app that I might actually like to use - so I strayed from my original plans for this project and focused on features that my beta-tester (aka *me*) actually wanted.  I tried to reorganize the site to be lighter-weight, with more information displayed more clearly.  And made sure that progress logs were editable from many places.


## Recommended Steps for Testing the App:
* Register.
* Make a New Goal - name it anything, but set a target quantity of ~10,000.
* Navigate to the goal's page, and then upload the test-csv file I've provided (example_progress_log.txt) to populate the goal with some data.

## Key Files/Directories

#### templates/goals/home.html
This is the landing page, mainly just displays your active goals.  Note that each goal displays recently added progress logs which can be edited in place.  Adding this feature was the moment I realized that I needed to refocus on a lightweight fast and easy-to-use app.

#### templates/goals/goal_view.html
 This is the heavy lifting view/template for the app.  There are four main components:
 * The Progress list: each individual log is editable in place via a AJAX request.  It will also live update the chart when you edit the progress here.
 * The Graphical View:  I used chart.js to configure the chart. In  hindsight I wish I'd chosen something heavier-weight; chart-js is pretty limited, especially with overlaying multiple plots onto the same chart area.  
 * The Progress-Entry Form:  This is the default form for adding progress to the goal.  Added option to submit up to three updates at once, because my beta-tester (aka me) found that useful
 * The CSV form submission to bulk-uploading.  This was not a planned feature, but I wanted to upload my google spreadsheet goal data onto this - so I wrote this option in!

#### templates/goals/new_goal.html
Page for making a new goal.  I made some of my first forays into JQuery working on this page, which I found useful working on the rest of the project.  This page is a little barebones since I removed the second type of goal, but it's snappy and responsive, so I kind of like it.  

#### templates/goals/layout.html

My django layout page for the main section of the site.  Nothing very fancy.  A little bit of logic to customize display based on who, if anyone, is logged in.  A navbar adapted from bootstrap.  Also links to the script sheets for chart.js.  And my boyfriend ~~demanded~~ **suggested** I use a fancy custom font for the site, so that is imported here!

#### Models.py

* I used the PolymorphicModel package for django so that I could have different classes of the base goal model and still be able to iterate over all the different types at once.  Since removing the Milestone goal types, the PolymorphicModel system is a little redundant, but I've left it in so that I can continue to tinker.

#### admin.py

* The admin page looks a little different because of how Polymorphic models need to be registered. The result is pretty familiar.  The ability to filter goals and goal progress at the default admin page is extremely useful

#### exampe_progress_log.txt

* A csv of a sample progress log that I used for testing the csv-upload feature.  Included in case you'd like to test the same.  Note that the log includes 8300 repetitions, so I recommend testing it with a goal that requires about 10,000 repetitions.  


#### temp.txt

* Used to temporarily store uploaded csv file text before it gets loaded into the database. Not strictly necessary - left in because of how often it has been useful in debugging.
