var CriticalInfoCard = {
    name: 'CriticalInfoCard',
    dom_target: undefined,
    render_init: function () {
        WSData.fetch_notice_data(CriticalInfoCard.render_upon_data, CriticalInfoCard.render_error);
    },
    render_upon_data: function () {
        if (!CriticalInfoCard._has_all_data()) {
            return;
        }
        CriticalInfoCard._render();
    },

    _has_all_data: function () {
        if (WSData.notice_data()) {
            return true;
        }
        return false;
    },

    _render: function () {
        var source = $("#ns_critical_info").html();
        var template = Handlebars.compile(source);
        var notices = Notices.get_notices_for_tag("checklist_email");
        if (notices.length > 0){
            CriticalInfoCard.dom_target.html(template({'notices': notices}));
        } else {
            CriticalInfoCard.dom_target.hide()
        }

    },
    render_error: function () {
        CriticalInfoCard.dom_target.html(CardWithError.render(CriticalInfoCard.name));
    },
};
