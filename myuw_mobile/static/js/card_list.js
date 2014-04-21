var Card_list = {
    show_list: function() {

        var source = $("#card_list").html();
        var template = Handlebars.compile(source);
        var notice_card = NoticeCard.render_card();
        var reg_status_card = RegStatusCard.render_card();

        $("#courselist").html(template({
            notice_card: notice_card,
            reg_status_card: reg_status_card
        }));

    }
};
