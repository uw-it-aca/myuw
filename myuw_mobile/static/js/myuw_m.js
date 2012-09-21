// mobile javascript
var data;

$(document).ready(function() {

    var course_data = null;
    var book_data = null;


    //probably extraneous
    Handlebars.registerHelper("formatTime", function(time) {
        formatted = time.toString().split(":");
        formatted[0] = parseInt(formatted[0], 10);
        if (formatted[0] > 12) {
            formatted[0] -= 12;
        }
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

        if (formatted[0] > 12) {
            formatted[0] = formatted[0] - 12;
        }
        return formatted.join(":");
    });

    Handlebars.registerHelper("ucfirst", function(str) {
        return str.replace(/^([a-z])/, function(match) {
            return match.toUpperCase();
        });
    });

    Handlebars.registerHelper("formatPrice", function(price) {
        formatted = price.toString().split(".");
        if (formatted[1] && formatted[1].length == 1) {
            formatted[1] += "0";
        }
        return formatted.join(".");
    });

    Handlebars.registerHelper('equal', function(value1, value2, options) {
        if (arguments.length < 3)
            throw new Error("Handlebars Helper equal needs 2 parameters");
        if(value1 != value2) {
            return options.inverse(this);
        } 
        else {
            return options.fn(this);
        }
    });

    History.Adapter.bind(window,'statechange',function(){
        var history_state = History.getState();
        var data = history_state.data;
        var state = data.state;

        if (state === undefined) {
            show_page_from_url();
        }
        else if (state === "course_list") {
            // Figure out what to do from the url
            CourseList.show_list(data.course_index);
        }
        else if (state === "instructor") {
            Instructor.show_instructor(data.instructor);
        }
        else if (state === "textbooks") {
            TextBooks.show_books();
        }
        else if (state === "quicklinks") {
            QuickLinks.show_links();
        }
        else if (state === "visual") {
            VisualSchedule.show_visual_schedule(data.course_index);
        }
    });

    function show_page_from_url() {
        var path = window.location.pathname;

        var hist = window.History;

        // The replaceState is for MUWM-368
        if (path === "/mobile/") {
            hist.replaceState({
                state: "course_list",
                }, "", "/mobile"
            );
            //CourseList.show_list();
        }
        else if (path.match("/mobile/visual")) {
            var matches = path.match(/^\/mobile\/visual\/([0-9]+)/);
            if (matches) {
                hist.replaceState({
                    state: "visual",
                    course_index: matches[1]
                },  "", "/mobile/visual");
                //VisualSchedule.show_visual_schedule(matches[1]);
            }
            else {
                hist.replaceState({
                    state: "visual"
                },  "", "/mobile/visual");
                //VisualSchedule.show_visual_schedule();
            }
        }
        else if (path === "/mobile/textbooks") {
            hist.replaceState({
                state: "textbooks"
            },  "", "/mobile/textbooks");
            //TextBooks.show_books();
        }
        else if (path === "/mobile/textbooks") {
            hist.replaceState({
                state: "textbooks"
            },  "", "/mobile/textbooks");
            //TextBooks.show_books();
        }
        else if (path === "/mobile/links") {
            hist.replaceState({
                state: "quicklinks"
            },  "", "/mobile/links");
            //QuickLinks.show_links();
        }
        else if (path.match(/^\/mobile\/instructor\/[A-Z0-9]+/)) {
            var matches = path.match(/^\/mobile\/instructor\/([A-Z0-9]+)/);
            hist.pushState({
                state: "instructor",
                instructor: matches[1]
            },  "", "/mobile/instructor/"+matches[1]);

//            Instructor.show_instructor(matches[1]);
        }
        else {
            // Just fall back to the course list?
            hist.replaceState({
                state: "course_list",
                }, "", "/mobile"
            );
            //CourseList.show_list();
        }
        History.Adapter.trigger(window, 'statechange');
    }


    show_page_from_url();

    $(".quicklinks").bind("click", function(ev) {
        $("#myuw_nav").collapse('hide');
        var hist = window.History;
        hist.pushState({
            state: "quicklinks",
        },  "", "/mobile/links");

        return false;
    });


    

});
