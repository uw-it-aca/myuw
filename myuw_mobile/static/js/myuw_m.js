// mobile javascript
var data;

$(document).ready(function() {

    $.ajax({
        url: "/my/api/v1/schedule/current/",
        dataType: "JSON",

        type: "GET",
        accepts: {html: "text/html"},
        success: function(results){
            if(results !== null){
                data = results;

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

                var source   = $("#courses").html();
                var template = Handlebars.compile(source);
                $("#courselist").html(template(data));

                source = $("#quarter").html();
                template = Handlebars.compile(source);
                $("#quarter-info").html(template({year: data.year, quarter: data.quarter}));
            }
        },
        error: function(xhr, status, error){
            //xhr+" "+status+" "+error);
        }
    });

});
