var InternationalStuCard = {
    name: 'InternationalStuCard',
    dom_target: undefined,

    render_init: function() {
        WebServiceData.require({notice_data: new NoticeData()}, InternationalStuCard.render);
    },

    render: function (resources) {
        var notice_resource = resources.notice_data;
        if (InternationalStuCard.render_error(notice_resource.error)) {
            return;
        }

        var source = $("#ns_international_stu").html();
        var template = Handlebars.compile(source);
        var notices = Notices.get_notices_for_tag("checklist_fiuts");
        if (notices.length > 0){
            InternationalStuCard.dom_target.html(template({'notices': notices}));
            LogUtils.cardLoaded(InternationalStuCard.name, InternationalStuCard.dom_target);
        } else {
            InternationalStuCard.dom_target.hide();
        }
    },

    render_error: function (notice_resource_error) {
        if (notice_resource_error) {
            InternationalStuCard.dom_target.html(CardWithError.render("International Student Resources"));
            return true;
        }

        return false;
    },
};
