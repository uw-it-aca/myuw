var ManageEmailLists = {
    name: 'ManageEmailLists',
    dom_target: undefined,
    label: undefined,

    render_init: function(section_label) {
        ManageEmailLists.label = section_label;
        ManageEmailLists.dom_target = '#manage_emaillist_' + safe_label(ManageEmailLists.label);
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
        var source   = $("#manage_email_lists_tmpl").html();
        var template = Handlebars.compile(source);
        var raw = template(data);
        $(ManageEmailLists.dom_target).html(raw);
        LogUtils.cardLoaded(ManageEmailLists.name, ManageEmailLists.dom_target);
    }
};
