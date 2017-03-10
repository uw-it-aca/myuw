var RequestEmailLists = {
    name: 'RequestEmailLists',
    dom_target: undefined,
    label: undefined,

    render_init: function(section_label) {
        RequestEmailLists.label = section_label;
        RequestEmailLists.dom_target = '#popup_emaillist_' + safe_label(RequestEmailLists.label);
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

        RequestEmailLists.add_events($(RequestEmailLists.dom_target));
    },

    add_events: function(panel) {
        var label = safe_label(RequestEmailLists.label);

        $('#select_all', panel).click(function(ev) {
            WSData.log_interaction("select_all_on_request_emaillist_"+label);
            if(this.checked) {
                $(':checkbox').each(function() {
                    this.checked = true;
                });
            } else {
                $(':checkbox').each(function() {
                    this.checked = false;
                });
            }
        });

        $(panel).find("button:submit").on("click", function(ev) {
            ev.preventDefault();
            var target = $(ev.currentTarget).closest('form');
            // Don't POST if no boxes are checked
            if(!RequestEmailLists.form_has_checked(target)){
                return;
            }
            WSData.log_interaction("submit_request_emaillist_form_"+label);
            $.ajax({
                url: "/api/v1/emaillist/",
                dataType: "JSON",
                async: true,
                type: 'POST',
                accepts: {html: "text/html"},
                data: $(target).serialize(),
                success: function(results) {
                    if (results.none_selected) {
                        RequestEmailLists.render();
                        return false;
                    }
                    var source = $("#request_email_lists_tmpl").html();
                    var template = Handlebars.compile(source);
                    results.netid = window.user.netid;
                    var raw = template(results);
                    $(RequestEmailLists.dom_target).html(raw);
                },
                error: function(xhr, status, error) {
                    raw = CardWithError.render("Submit email list: " + error);
                    $(RequestEmailLists.dom_target).html(raw);
                    return false;
                }
            });
        });
    },

    form_has_checked: function(target){
        var checked = $(target).find(":checked");
        return checked.length > 0;
    }
};
