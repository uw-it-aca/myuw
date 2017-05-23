var ManageEmailLists = {
    name: 'ManageEmailLists',
    dom_target: undefined,
    label: undefined,

    render_init: function(section_label) {
        ManageEmailLists.label = section_label;
        ManageEmailLists.dom_target = '#popup_emaillist_' + safe_label(ManageEmailLists.label);

        WebServiceData.require({section_emaillist_data: new InstructedSectionEmailListData()},
                               ManageEmailLists.render);
    },

    render_error: function(section_emaillist_resource_error) {
        if (section_emaillist_resource_error && section_emaillist_resource_error.status === 543) {
            raw = CardWithError.render("Request Email List Popup");
            $(ManageEmailLists.dom_target).html(raw);
            return true;
        }

        return false;
    },

    render: function(resources) {
        var section_emaillist_resource = resources.section_emaillist_data;

        if (ManageEmailLists.render_error(section_emaillist_resource.error)) {
            return;
        }

        var data = section_emaillist_resource.data;
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
            WSData.log_interaction("switch_to_create_email_list_"+label);
            return false;
        });
    }
};
