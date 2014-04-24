var Landing = {
    render: function() {
        showLoading();
        WSData.fetch_notice_data(Landing.make_html);
    },
    make_html: function() {
        var notice_data = WSData.notice_data();
        var source = $("#landing").html();
        var template = Handlebars.compile(source);

        var notice_banner = NoticeBanner.render(notice_data);
        var reg_status_card = RegStatusCard.render(notice_data);

        $("#courselist").html(template({
            notice_banner: notice_banner,
            reg_status_card: reg_status_card
        }));

    }
};
