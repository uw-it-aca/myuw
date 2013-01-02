var Quarters = {
    show_future_quarters: function() {
        showLoading();
        WSData.fetch_oquarter_data(Quarters.render_registered_future_quarters);
    },

    render_registered_future_quarters: function() {
        $('html,body').animate({scrollTop: 0}, 'fast');
        
        var source = $("#oquarter-header").html();
        var template = Handlebars.compile(source);
        $("#page-header").html(template());

        var data = WSData.oquarter_data();

        if (data.terms.length == 0) {
            $("#courselist").no_courses({
                "which_quarter_or_term" : "in future quarters",
                "present_addi_links" : false
            });
            return;
        }
        var urlprefix = "/mobile";
        var path = window.location.pathname;
        var matches = path.match(/^\/mobile\/future_quarters(\/.*)$/);
        if (matches) {
            urlprefix = urlprefix + matches[1]
        }

        source = $("#quarterlist").html();
        template = Handlebars.compile(source);
        $("#courselist").html(template({ 
            "urlprefix" : urlprefix,
            "terms" : data.terms }));
    }
};
