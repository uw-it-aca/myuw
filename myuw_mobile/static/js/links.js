var QuickLinks = {
    show_links: function() {
        window.setTimeout(QuickLinks.render_links, 0);
    },

    render_links: function() {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var source   = $("#quicklinks").html();
        var template = Handlebars.compile(source);

        $("#courselist").html(template());
    }
};
