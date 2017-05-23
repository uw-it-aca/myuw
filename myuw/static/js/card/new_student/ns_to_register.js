var ToRegisterCard = {
    name: 'ToRegisterCard',
    dom_target: undefined,
    render_init: function () {
        WebServiceData.require({notice_data: new NoticeData()},
                               ToRegisterCard.render);
    },

    render: function (resources) {
        var notice_resource = resources.notice_data;
        if (ToRegisterCard.render_error(notice_resource.error)) {
            return;
        }

        var source = $("#ns_to_register").html();
        var template = Handlebars.compile(source);
        var no_orient = Notices.get_notices_for_tag("checklist_no_orient");
        var post_orient = Notices.get_notices_for_tag("checklist_orient_after");
        var pre_iss = Notices.get_notices_for_tag("checklist_iss_before");
        var post_iss = Notices.get_notices_for_tag("checklist_iss_after");
        var pre_measles = Notices.get_notices_for_tag("checklist_measles_before");
        var post_measles = Notices.get_notices_for_tag("checklist_measles_after");
        var pre_orient = Notices.get_notices_for_tag("checklist_orient_before");
        var no_orient_date = false;

        if (no_orient.length > 0) {
            no_msg = no_orient[0];
            $.each(no_msg.attributes, function(idx, attrib){
                if(attrib.name === "Date") {
                    no_orient_date = attrib.formatted_value;
                }

            });
        }

        if (ToRegisterCard.has_to_register_notices()){
            ToRegisterCard.dom_target.html(template({'no_orient': no_orient,
                                                     'no_orient_date': no_orient_date,
                                                     'post_orient': post_orient,
                                                     'pre_iss': pre_iss,
                                                     'post_iss': post_iss,
                                                     'pre_measles': pre_measles,
                                                     'post_measles': post_measles,
                                                     'pre_orient': pre_orient}));
            LogUtils.cardLoaded(ToRegisterCard.name, ToRegisterCard.dom_target);
        } else {
            ToRegisterCard.dom_target.hide();
        }

    },

    render_error: function (notice_resource_error) {
        if (notice_resource_error) {
            ToRegisterCard.dom_target.html(CardWithError.render("To Register for Classes"));
            return true;
        }

        return false;
    },

    has_to_register_notices: function () {
        var no_orient = Notices.get_notices_for_tag("checklist_no_orient");
        var post_orient = Notices.get_notices_for_tag("checklist_orient_after");
        var pre_iss = Notices.get_notices_for_tag("checklist_iss_before");
        var post_iss = Notices.get_notices_for_tag("checklist_iss_after");
        var pre_measles = Notices.get_notices_for_tag("checklist_measles_before");
        var post_measles = Notices.get_notices_for_tag("checklist_measles_after");
        var pre_orient = Notices.get_notices_for_tag("checklist_orient_before");

        var notice_count =  no_orient.length +
            post_orient.length +
            pre_iss.length +
            post_iss.length +
            pre_measles.length +
            post_measles.length +
            pre_orient.length;
        return notice_count > 0;

    }
};
