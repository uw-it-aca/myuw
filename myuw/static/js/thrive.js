var Thrive = {
    show_content: function() {
        "use strict";
        var source = $("#thrive_content").html();
        var template = Handlebars.compile(source);
        $("#main-content").html(template());
    }
};


var ThriveMessages = {
    show_content: function() {
        "use strict";
        var source = $("#thrive_messages").html();
        var template = Handlebars.compile(source);
        $("#main-content").html(template());
    }
};


