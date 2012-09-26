var QuickLinks = {
    show_links: function() {
        WSData.fetch_link_data(QuickLinks.render_links);
    },

    render_links: function() {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var source   = $("#quicklinks").html();
        var template = Handlebars.compile(source);

        var links = WSData.link_data();
        $("#courselist").html(template({ links: links }));

        $("#edit_links").bind("click", function(ev) {
            $("#link_display_pane").hide();
            $("#link_edit_pane").show();
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
