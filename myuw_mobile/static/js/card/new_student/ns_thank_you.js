var ThankYouCard = {
    name: 'ThankYouCard',
    dom_target: undefined,
    render_init: function() {
        WSData.fetch_notice_data(ThankYouCard.render_upon_data,ThankYouCard.render_error);
    },
        render_upon_data: function() {
        if (!ThankYouCard._has_all_data()) {
            return;
        }
        ThankYouCard._render();
    },

    _has_all_data: function () {
        if (WSData.notice_data()) {
            return true;
        }
        return false;
    },

    _render: function () {
        var source = $("#ns_thank_you").html();
        var template = Handlebars.compile(source);
        var notices = Notices.get_notices_for_tag("checklist_thankyou");

        ThankYouCard.dom_target.html(template({'notices': notices}));
    },
    render_error: function () {
        ThankYouCard.dom_target.html(CardWithError.render(ThankYouCard.name));
    },
};
