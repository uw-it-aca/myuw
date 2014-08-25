var NoticeBanner = {
    dom_target: undefined,

    render_init: function(dom_taget) {
        NoticeBanner.dom_target  = dom_taget;
        WSData.fetch_notice_data(NoticeBanner.render);
    },

    render: function () {
        var notice_data = WSData.notice_data();

        if (notice_data.length > 0) {
            var source = $("#notice_banner").html();
            var template = Handlebars.compile(source);

            var html = template({
                "total_unread": Notices.get_total_unread(),
                "total_critical": Notices.get_all_critical()
            });
            NoticeBanner.dom_target.html(html);
        }
        
        
        // handle clicking on resources
        $("#categories_link").bind("click", function(ev) {
            ev.preventDefault();                
            $('html, body').animate({
                scrollTop: $("#categories").offset().top
            }, "fast");
            return false;
        });
    

    }
};

