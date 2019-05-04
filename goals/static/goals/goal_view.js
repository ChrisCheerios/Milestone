document.addEventListener('DOMContentLoaded', () => {
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
                    label: 'goal_units',
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
