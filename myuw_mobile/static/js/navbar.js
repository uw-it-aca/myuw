var Navbar = {
    render_navbar: function(navbar_type) {
        if (navbar_type === "nav-sub") {
            source = $("#nav-sub").html();
        } else {
            //defaulting to the 'standard' navbar
            source = $("#nav").html();
        }
        template = Handlebars.compile(source);
        $("#navbar").html(template({'netid': window.user.netid}));
    }
}