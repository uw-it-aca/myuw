var Thrive = {
    show_content: function() {
        "use strict";
        var source = $("#thrive_content").html();
        var template = Handlebars.compile(source);
        $("#main-content").html(template());
    }
};


var ThriveMessages = {
    show_messages: function() {
        "use strict";
        CommonLoading.render_init();
        WSData.fetch_thrive_data_history(ThriveMessages.render_messages);
    },

    render_messages: function() {
        "use strict";
        Handlebars.registerPartial('thrive_highlight', $("#thrive_highlight").html());
        Handlebars.registerPartial('thrive_learnmore', $("#thrive_learnmore").html());
        var messages = WSData.thrive_data();
        var source = $("#thrive_messages").html();
        var template = Handlebars.compile(source);
        var message_groups = ThriveMessages.message_groups(messages, 2);

        $("#main-content").html(template({ message_groups: message_groups }));
    },

    message_groups: function(messages, per_row){
        var source = $("#thrive_message").html();
        var template = Handlebars.compile(source);
        var groups = [];
        var group = [];
        var i;

        for (i = 0; i < messages.length; i += 1) {
            if (i > 0 && i % per_row === 0) {
                groups.push(group);
                group = [];
            }

            group.push(template(messages[i]));
        }

        groups.push(group);

        return groups;
    }
};


