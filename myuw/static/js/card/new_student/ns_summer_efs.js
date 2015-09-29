var SummerEFSCard = {
    name: 'SummerEFSCard',
    dom_target: undefined,
    render_init: function () {
        WSData.fetch_notice_data(SummerEFSCard.render_upon_data, SummerEFSCard.render_error);
    },
    render_upon_data: function () {
        if (!SummerEFSCard._has_all_data()) {
            return;
        }
        SummerEFSCard._render();
    },

    _has_all_data: function () {
        if (WSData.notice_data()) {
            return true;
        }
        return false;
    },

    _render: function () {
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
    render_error: function () {
        SummerEFSCard.dom_target.html(CardWithError.render(SummerEFSCard.name));
    },
};
