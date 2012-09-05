// mobile javascript
var data;

$(document).ready(function() {

    var course_data = null;
    var book_data = null;


    //probably extraneous
    Handlebars.registerHelper("formatTime", function(time) {
        formatted = time.toString().split(":");
        formatted[0] = parseInt(formatted[0], 10);
        return formatted.join(":");
    });

    //converts 24 hour time to 12 hour
    Handlebars.registerHelper("formatTimeAMPM", function(time) {
        formatted = time.toString().split(":");
        formatted[0] = parseInt(formatted[0], 10);
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

        if (state === null || state === "course_list") {
            // Figure out what to do from the url
            show_page_from_url();
        }
        else if (state === "instructor") {
            Instructor.show_instructor(data.instructor);
        }
        else if (state === "visual") {
            VisualSchedule.show_visual_schedule();
        }
    });

    function show_page_from_url() {
        var path = window.location.pathname;

        if (path === "/my/") {
            CourseList.show_list();
        }
        else if (path === "/my/visual") {
            VisualSchedule.show_visual_schedule();
        }
        else if (path.match(/^\/my\/instructor\/[A-Z0-9]+/)) {
            var matches = path.match(/^\/my\/instructor\/([A-Z0-9]+)/);
            Instructor.show_instructor(matches[1]);
        }
        else {
            // Just fall back to the course list?
            CourseList.show_list();
        }
    }

    show_page_from_url();


});
