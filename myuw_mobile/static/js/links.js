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
        });

        $("#save_links").bind("click", function(ev) {
            QuickLinks.save_links();
        });

        $("#save_links_bottom").bind("click", function(ev) {
            QuickLinks.save_links();
        });
    },

    save_links: function() {
        var links = WSData.link_data();

        links[1].is_on = true;
        links[2].is_on = true;
        links[3].is_on = true;

        QuickLinks.render_links();
    }
};
