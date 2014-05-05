var QuickLinks = {
    show_links: function() {
        showLoading();
        WSData.fetch_link_data(QuickLinks.render_links);
    },

    render_links: function() {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var source   = $("#quicklinks").html();
        var template = Handlebars.compile(source);
        var head_template = Handlebars.compile($("#quicklinks-header").html());
        $("#page-header").html(head_template());

        var links = WSData.link_data();
        $("#main-content").html(template({ links: links }));

        $("#edit_links").bind("click", function(ev) {
            $("#link_display_pane").hide();
            $("#link_edit_pane").show();

            $("#link_header_view").hide();
            $("#link_header_edit").show();
            return false;
        });

        $("#save_links").bind("click", function(ev) {
            QuickLinks.save_links();
            return false;
        });

        $("#save_links_bottom").bind("click", function(ev) {
            QuickLinks.save_links();
            return false;
        });

        var index = 0;
        // This is a workaround for MUWM-427
        // From: http://stackoverflow.com/questions/7358781/tapping-on-label-in-mobile-safari
        for (index = 0; index < links.length; index++) {
            var link = links[index];
            $("#link"+link.id+"label").bind("click", function() { });
        }
    },

    save_links: function() {
        var links = WSData.link_data();

        var i = 0;
        for (i = 0; i < links.length; i++) {
            var link = links[i];
            var check = $("#link"+link.id);
            if (check.is(':checked')) {
                links[i].is_on = true;
            }
            else {
                links[i].is_on = false;
            }
        }

        WSData.save_links(links);

        QuickLinks.render_links();
    }
};
