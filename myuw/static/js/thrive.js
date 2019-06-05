var Thrive = {
    show_content: function() {
        "use strict";
        var source = $("#thrive_content").html();
        var template = Handlebars.compile(source);
        $("#main-content").html(template(Thrive.set_target({})));
    },

    set_target: function(data) {
        if (window.user.fyp) {
            data.target_fyp = true;
        }
        if (window.user.aut_transfer) {
            data.target_aut_transfer = true;
        }
        if (window.user.win_transfer) {
            data.target_win_transfer = true;
        }
        return data;
    },
};


var ThriveMessages = {
    show_messages: function() {
        "use strict";
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
        data = {message_groups: message_groups};
        $("#main-content").html(template(Thrive.set_target(data)));
    },

    message_groups: function(messages, per_row){
        var source = $("#thrive_message").html();
        var template = Handlebars.compile(source);
        var groups = [];
        var group = [];
        var i;

        for (var i = 0; i < messages.length; i += 1) {
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


