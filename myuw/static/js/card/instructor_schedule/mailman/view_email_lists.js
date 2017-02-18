var ManageEmailLists = {
    name: 'ManageEmailLists',
    dom_target: undefined,
    label: undefined,

    render_init: function(section_label) {
        ManageEmailLists.label = section_label;
        ManageEmailLists.dom_target = '#popup_emaillist_' + safe_label(ManageEmailLists.label);
        WSData.fetch_instructed_section_emaillist_data(section_label,
                                                       ManageEmailLists.render_upon_data,
                                                       ManageEmailLists.render_error);
    },

    render_upon_data: function() {
        if (WSData._instructed_emaillist_data[ManageEmailLists.label] === undefined) {
            return;
        }
        ManageEmailLists.render();
    },

    render_error: function() {
        var error_code = WSData._instructed_emaillist_data_error_status[ManageEmailLists.label];
        if (error_code == 543) {
            raw = CardWithError.render("Request Email List Popup");
            $(ManageEmailLists.dom_target).html(raw);
        }
    },


    render: function() {
        var data = WSData._instructed_emaillist_data[ManageEmailLists.label];
        var term = data.year + ',' + data.quarter;
        var source   = $("#manage_email_lists_tmpl").html();
        var template = Handlebars.compile(source);
        var raw = template(data);
        $(ManageEmailLists.dom_target).html(raw);
        LogUtils.cardLoaded(ManageEmailLists.name, ManageEmailLists.dom_target);
        ManageEmailLists.add_events();
    },

    add_events: function() {
        var label = safe_label(ManageEmailLists.label);

        $("#switch_to_create_email_list").on("click", function(ev) {
            RequestEmailLists.render_init(ManageEmailLists.label);
            WSData.log_interaction("switch_to_create_email_list", label);
            return false;
        });
    }
};
