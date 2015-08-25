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

        if (data.terms.length === 0) {
            $("#main-content").no_courses({
                "which_quarter_or_term" : "in future quarters",
                "show_future_link" : false
            });
            return;
        }

        var urlprefix = "/";
        var path = window.location.pathname;
        var matches = path.match(/^\/future_quarters(\/.*)$/);
        if (matches) {
            urlprefix = urlprefix + matches[1];
        }

        var is_visual = false;
        if (urlprefix === "/visual") {
            is_visual = true;
        }

        source = $("#quarterlist").html();
        template = Handlebars.compile(source);
        $("#main-content").html(template({ 
            "urlprefix" : urlprefix,
            "terms" : data.terms }));

        $(".show_future_term").bind("click", function(ev) {
            var term = ev.target.rel.replace(/^\//, '');
            var state = {
                state: is_visual ? "visual" : "course_list",
                term: term
            };

            var url;
            if (is_visual) {
                url = "/visual/"+term;
            }
            else {
                url = "/"+term;
            }
            var hist = window.History;
            hist.pushState(state, "", url);

            return false;
        });


    }
};
