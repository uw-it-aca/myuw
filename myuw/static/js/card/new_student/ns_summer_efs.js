var SummerEFSCard = {
    name: 'SummerEFSCard',
    dom_target: undefined,
    render_init: function () {
        WebServiceData.require({notice_data: new NoticeData()},
                               SummerEFSCard.render);
    },

    render: function (resources) {
        var notice_resource = resources.notice_data;
        if (SummerEFSCard.render_error(notice_resource.error)) {
            return;
        }

        var source = $("#ns_summer_efs").html();
        var template = Handlebars.compile(source);
        var notices = Notices.get_notices_for_tag("checklist_summerreg");
        if (ToRegisterCard.has_to_register_notices()){
            SummerEFSCard.dom_target.html(template({'notices': notices}));
            LogUtils.cardLoaded(SummerEFSCard.name, SummerEFSCard.dom_target);
        } else {
            SummerEFSCard.dom_target.hide();
        }
    },

    render_error: function (notice_resource_error) {
        if (notice_resource_error) {
            SummerEFSCard.dom_target.html(CardWithError.render("Summer & Early Fall Start"));
            return true;
        }

        return false;
    },
};
