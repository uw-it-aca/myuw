// mobile javascript
var data;

$(document).ready(function() {

    var course_data = null;
    var book_data = null;

    function fetch_course_data(callback, args) {
        if (course_data == null) {
            $.ajax({
                url: "/my/api/v1/schedule/current/",
                dataType: "JSON",

                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    course_data = results;
                    callback.apply(null, args);
                },
                error: function(xhr, status, error) {
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    }

    /* Methods for the initial page load */
    function show_list() {
        fetch_course_data(render_list);
    }

    function render_list() {
        var source   = $("#courses").html();
        var template = Handlebars.compile(source);
        $("#courselist").html(template(course_data));

        source = $("#quarter").html();
        template = Handlebars.compile(source);
        $("#quarter-info").html(template({year: course_data.year, quarter: course_data.quarter}));

        $(".instructor").bind("click", function(ev) {
            var hist = window.History;
            hist.pushState({
                state: "instructor",
                instructor: ev.target.rel
            },  "", "/my/instructor/"+ev.target.rel);
        });

    }

    /* Methods for showing an instructor */
    function show_instructor(regid) {
        fetch_course_data(render_instructor, [regid]);
    }

    function render_instructor(regid) {
        alert("Show instructor: "+regid);
    }

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
            show_list();
        }
        else if (state === "instructor") {
            show_instructor(data.instructor);
        }
    });

    show_list();

});
