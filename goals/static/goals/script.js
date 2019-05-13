
/*
This function (borrowed from stackexchange) formats a date object so it can be
 inputted into the html form.  Used below to set the default date to 'today'
*/
Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
});



document.addEventListener('DOMContentLoaded', () => {

    // Configures the Form Display for Adding new Journey Goal
    $('#show_journey_form').on('click', function () {
        console.log("GOTEM")
        $('.hide_journey').show();
        $('.hide-flex').css( "display", "flex" );
        $('.show').hide();
    })

    // Configures the Form Display for Adding new Journey Goal
    $('#show_milestone_form').on('click', function () {
        console.log("GOTEM")
        $('.hide_milestone').show();
        $('.hide-flex').css( "display", "flex" );
        $('.show').hide();
    })

    // Configures button to reveal/hide sections of the page
    $('.closer').on('click', function () {
        $('.hide').hide();
        $('.show').show();
    });

    // Set the default date in the input fields to today
    $('.date').val(new Date().toDateInputValue());

    // This marks if the date-change alert message has not been shown (True = not yet shown)
    let alert_Bool = true;

    // This event listener marks if user starts to record progress for a future date.
    // Ideally users will only log already-completed progress, but they are free to do what they like!
    $('.date').on('change', function() {
        let today = new Date().toDateInputValue()
        let date = this.value
        if (date > today && alert_Bool) {
            alert("We advise only logging past progress, and not future progress! This message will not show again until you leave the page.")
            alert_Bool = false;
        }
    });

    // Configure the edit button for my goal_view page to make the progress logs editable
    $(".edit").on('click', function () {
        $(this).parent().hide()
        $(this).parent().next().show()
    })

    // Configure the button to close the progress-edit options
    $(".progress-cancel").on('click',function() {
        $(this).parent().parent().parent().hide()
        $(this).parent().parent().parent().prev().show()
    })


    // Configure my progress-edit buttons to call the progress_update() function
    // n.b. this is used on multiple pages.
    $(".progress_edit").submit(function(e) {

        // Stop the form submission
        e.preventDefault();

        // Serialize the data from the form for the AJAX requets
        let data = $(this).serialize()

        // Grab the form-data so that the log can be updated
        let goal = this.goal_id.value
        let id = this.progress_id.value
        let new_date = this.date_edit.value
        let new_quantity = this.quantity_edit.value

        // Make the ajax requets to the API endpoint for the goal
        jQuery.ajax({
            method: "POST",
            url: `/api/data/${goal}`,
            data: data
        })
        .done(function(msg) {
            console.log(msg)
            update_chart()
            // This string is specific to the goal_id and progress_id.  Used to
            // identify which log to update
            string = "#" + `${goal}` + `_${id}` + "_text"
            $(`${string}`).text(`Updated: ${new_date}: ${new_quantity}`);
        });

    });


    // Declare my chart.  This needs to be global
    var chart

    // <!-- The endpoint for the API call to update the chart-->
    var endpoint = `/api/data/${goal_id}`

    // <!-- This is the function that updates the chart with most recent data -->
    function update_chart() {
        $.ajax({
            method: "GET",
            url: endpoint,
            success: function(data) {
                dates = data.dates
                // Add the date for the final Goal as a label for the last column
                dates.push( "Final Goal")
                // The progress values for each log entry
                progress = data.progress
                // Add the total target goal for the value of the last column
                // note that goal_total is declared in the template
                progress.push(goal_total)

                cumulative_progress = data.cumulative_progress
                chart_update()
            },
            error: function(error) {
                console.log("error")
                console.log(error)
            }
        });
    };

    // <!-- The function that updates the chart itself, with info from the ajax request above -->
    function chart_update (){

        // <!-- Destroy the Old Chart, if any -->
        if(chart){
            chart.destroy();
        }

        // <!-- Make a new chart -->

        // <!-- Grab the location for the chart -->
        let ctx = document.getElementById('myChart').getContext('2d');

        // <!-- Make the chart -->
        chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'bar',

            // The data for our dataset
            data: {
                labels: dates,
                datasets: [{
                    label: "Final Goal",
                    backgroundColor: 'rgb(23,82,42)',
                    borderColor: 'rgb(23,82,42)',
                    data: progress
                },
                {
                    label: 'Cumulative Progress',
                    backgroundColor: 'rgb(222, 242, 241)',
                    borderColor: 'rgb(222, 242, 241)',
                    data: cumulative_progress,
                    type: 'line'
                }
                ]
            },

            // Configuration options go here
            options: {
            }
        });
    };



    function showlist() {
        $("#full_list").show()
        $("#show_button").hide()
    };

    var button = document.querySelector('#show_more')
    button.addEventListener('click', show_more)

    function show_more() {
        $('.progress-block').css( "display", "flex" );
        this.style.display = 'none'
    }

    // Updates the Chart when the page loads
    update_chart()


});



// Configures the buttons to hide and show the full list of progress logs
function showlist() {
    $(".full_list").show()
    $("#show_button").hide()
}

function hidelist() {
    $(".full_list").hide()
    $("#show_button").show()

}
