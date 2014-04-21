var NoticeCard = {
    render_card: function () {
        var source = $("#notice_card").html();
        var template = Handlebars.compile(source);
        return template();
    }
};
