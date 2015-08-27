var InternationalStuCard = {
    name: 'InternationalStuCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_notice_data(InternationalStuCard.render_upon_data,InternationalStuCard.render_error);
    },

    render_upon_data: function() {
        if (!InternationalStuCard._has_all_data()) {
            return;
        }
        InternationalStuCard._render();
    },

    _has_all_data: function () {
        if (WSData.notice_data()) {
            return true;
        }
        return false;
    },

    _render: function () {
        var source = $("#ns_international_stu").html();
        var template = Handlebars.compile(source);
        var notices = Notices.get_notices_for_tag("checklist_fiuts");
        if (notices.length > 0){
            InternationalStuCard.dom_target.html(template({'notices': notices}));
        } else {
            InternationalStuCard.dom_target.hide();
        }
    },
    render_error: function () {
        InternationalStuCard.dom_target.html(CardWithError.render(InternationalStuCard.name));
    },
};
