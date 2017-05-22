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
                $(':checkbox:enabled').each(function() {
                    this.checked = true;
                });
            } else {
                $(':checkbox:enabled').each(function() {
                    this.checked = false;
                });
            }
        });
        $(".mailman_advanced_toggle").click(function(ev){
            $(".mailman_simple_create").hide();
            $(".mailman_advanced_toggle").hide();
            $(".mailman_simple_toggle").show();
            //Disable the single section input
            $(".mailman_simple_create").find("input").prop('disabled', true);
            $(".mailman_advanced_create").show();
            return false;
        });

        $(".mailman_simple_toggle").click(function(ev){
            $(".mailman_simple_create").show();
            $(".mailman_advanced_toggle").show();
            $(".mailman_simple_toggle").hide();
            //Disable the single section input
            $(".mailman_simple_create").find("input").prop('enabled', true);
            $(".mailman_advanced_create").hide();
            return false;
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
                    $("#request_emaillist_form").find(".modal-body").hide();
                    $("#request_emaillist_form").find("button:submit").hide();
                    $("#request_emaillist_form").find(".modal-error").show();
                    return false;
                }
            });
        });
    },

    form_has_checked: function(target){
        // test if single section modal
        var single_section = false;
        $(target).find(":hidden").each(function(idx, val){
            if($(val).attr("id") !== undefined && $(val).attr("id").indexOf("section_single") > -1){
                single_section =  true;
            }
        });
        if(single_section){
            return single_section;
        }

        var checked = $(target).find(":checked");
        return checked.length > 0;
    }
};
