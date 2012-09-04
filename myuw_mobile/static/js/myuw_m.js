// mobile javascript
var data;

$(document).ready(function() {

    var course_data = null;
    var book_data = null;


    //probably extraneous
    Handlebars.registerHelper("formatTime", function(time) {
        formatted = time.toString().split(":");
        formatted[0] = parseInt(formatted[0], 10)
        return formatted.join(":");
    });

    //converts 24 hour time to 12 hour
    Handlebars.registerHelper("formatTimeAMPM", function(time) {
        formatted = time.toString().split(":");
        formatted[0] = parseInt(formatted[0], 10)
        if (formatted[0] < 12) {
            formatted[1] += "AM";
        }
        else {
            formatted[1] += "PM";
        }
        return formatted.join(":");
    });


    History.Adapter.bind(window,'statechange',function(){
        var history_state = History.getState();
        var data = history_state.data;
        var state = data.state;

        if (state === null) {
            // Figure out what to do from the url
            CourseList.show_list();
        }
        else if (state === "instructor") {
            Instructor.show_instructor(data.instructor);
        }
        else if (state === "visual") {
            VisualSchedule.show_visual_schedule();
        }
    });

    CourseList.show_list();


});
