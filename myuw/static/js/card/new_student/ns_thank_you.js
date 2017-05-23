var ThankYouCard = {
    name: 'ThankYouCard',
    dom_target: undefined,
    render_init: function() {
        WebServiceData.require({notice_data: new NoticeData()},
                               ThankYouCard.render);
    },

    render: function (resources) {
        var notice_resource = resources.notice_data;
        if (ThankYouCard.render_error(notice_resource.error)) {
            return;
        }

        var source = $("#ns_thank_you").html();
        var template = Handlebars.compile(source);
        var ty_notices = Notices.get_notices_for_tag("checklist_thankyou");
        var fp_notices = Notices.get_notices_for_tag("checklist_feespaid");
        var notices  = ty_notices.concat(fp_notices);

        var notice_hashes = [];

        for (var i = 0; i < notices.length; i += 1) {
            var notice = notices[i];
            if (!notice.is_read) {
                notice_hashes.push(notice.id_hash);
            }
        }

        if (notice_hashes.length > 0){
            ThankYouCard.dom_target.html(template({'notices': notices}));
            ThankYouCard.mark_notices_read(notice_hashes);
            LogUtils.cardLoaded(ThankYouCard.name, ThankYouCard.dom_target);
        } else {
            ThankYouCard.dom_target.hide();
        }


    },
    render_error: function (notice_resource_error) {
        if (notice_resource_error) {
            ThankYouCard.dom_target.html(CardWithError.render("Payment Thank You"));
            return true;
        }

        return false;
    },

    mark_notices_read: function(notice_hashes) {
        WSData.mark_notices_read(notice_hashes);
    },
};
