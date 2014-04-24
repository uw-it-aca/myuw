var NoticeBanner = {
    render: function (notice_data) {


        var source = $("#notice_banner").html();
        var template = Handlebars.compile(source);
        return template();
    }
};
