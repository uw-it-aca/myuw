var RequestEmailLists = {
    name: 'RequestEmailLists',
    dom_target: undefined,
    label: undefined,

    render_init: function(section_label) {
        RequestEmailLists.label = section_label;
        RequestEmailLists.dom_target = '#request_emaillist_' + safe_label(RequestEmailLists.label);
        WSData.fetch_instructed_section_emaillist_data(section_label,
                                                       RequestEmailLists.render_upon_data,
                                                       RequestEmailLists.render_error);
    },

    render_upon_data: function() {
        if (WSData._instructed_emaillist_data[RequestEmailLists.label] === undefined) {
            return;
        }
        RequestEmailLists.render();
    },

    render_error: function() {
        var error_code = WSData._instructed_emaillist_data_error_status[RequestEmailLists.label];
        if (error_code == 543) {
            raw = CardWithError.render("Request Email List");
            $(RequestEmailLists.dom_target).html(raw);
        }
    },


    render: function() {
        var data = WSData._instructed_emaillist_data[RequestEmailLists.label];
        if (data.total_course_wo_list > 1) {
            data.multi_sections_wo_list = true;
        }
        var term = data.year + ',' + data.quarter;
        var source   = $("#request_email_lists_tmpl").html();
        var template = Handlebars.compile(source);
        var raw = template(data);
        $(RequestEmailLists.dom_target).html(raw);
        LogUtils.cardLoaded(RequestEmailLists.name, RequestEmailLists.dom_target);
        RequestEmailLists.add_events($(RequestEmailLists.dom_target), data.section_list.section_label, term);
    },

    add_events: function(panel, section_label, term) {
        var label = safe_label(section_label);

        $('#select_all', panel).click(function(ev) {
            if(this.checked) {
                $(':checkbox').each(function() {
                    this.checked = true;
                });
            } else {
                $(':checkbox').each(function() {
                    this.checked = false; 
                });
            }                
            WSData.log_interaction("checklist_select_all_" + label, term);
        });

        $("#request_emaillist_form", panel).on("submit", function(ev) {
            WSData.log_interaction("request_emaillist_form_submit_" + label, term);
            ev.preventDefault();
            var target = ev.currentTarget;
            $.ajax({
                url: "/api/v1/emaillist/",
                dataType: "JSON",
                async: true,
                type: 'POST',
                accepts: {html: "text/html"},
                data: $(target).serialize(),
                success: function(results) {
                    var data = results;
                    var source = $("#request_email_lists_tmpl").html();
                    var template = Handlebars.compile(source);
                    var raw = template(data);
                    $(RequestEmailLists.dom_target).html(raw);
                    LogUtils.cardLoaded('RequestEmailLists-submitted', RequestEmailLists.dom_target);
                },
                error: function(xhr, status, error) {
                    raw = CardWithError.render("Request Email List Submit");
                    $(RequestEmailLists.dom_target).html(raw);
                }
            });
        });
    }
};
