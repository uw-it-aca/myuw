// mobile javascript
var data;

$(document).ready(function() {
    regid = '9136CCB8F66711D5BE060004AC494FFE';

    $.ajax({
        url: "/my/api/v1/schedule/current/" + regid,
        dataType: "JSON",

        type: "GET",
        accepts: {html: "text/html"},
        success: function(results){
            if(results !== null){
                data = results;

                var source   = $("#courses").html();
                var template = Handlebars.compile(source);
                $("#courselist").html(template({sections: data.sections}));

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
