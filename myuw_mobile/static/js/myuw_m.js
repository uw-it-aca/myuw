// mobile javascript
var data;

$(document).ready(function() {

    var course_data = null;
    var book_data = null;

    function show_list() {
        fetch_course_data(render_list);
    }

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
                callback.apply(args);
            }, 0);
        }
    }

    function render_list() {
        var source   = $("#courses").html();
        var template = Handlebars.compile(source);
        $("#courselist").html(template(course_data));

        source = $("#quarter").html();
        template = Handlebars.compile(source);
        $("#quarter-info").html(template({year: course_data.year, quarter: course_data.quarter}));

        $(".instructor").bind("click", function(ev) {
            //console.log(ev.target.rel);
        });

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


    show_list();

/*
    $.ajax({
        url: "/my/api/v1/schedule/current/",
        dataType: "JSON",

        type: "GET",
        accepts: {html: "text/html"},
        success: function(results){
            show_list()

            if(results !== null){
                data = results;


            }
        },
        error: function(xhr, status, error){
            //xhr+" "+status+" "+error);
        }
    });
*/
});
