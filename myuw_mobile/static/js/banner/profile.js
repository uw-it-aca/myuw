var Profile = {
    render_upon_data: function() {
        var source = $("#profile-content").html();
        var template = Handlebars.compile(source);
        $("#profile").html(template(WSData.profile_data()));
        $("#toggle_my_profile").attr("title", $("#profile_toggle_hidden").text());
        Profile.add_events();
    },

    add_events: function() {
        $("#toggle_my_profile").on("click", function(ev) {
            ev.preventDefault();
            $("#my_profile").toggleClass("slide-show");

            if ($("#my_profile").hasClass("slide-show")) {
                $("#my_profile_arrow").attr('class', 'fa fa-chevron-up');
                $("#my_profile").attr('aria-hidden', 'false');
                $("#my_profile").show();
                $("#toggle_my_profile").attr("title", $("#profile_toggle_displayed").text());
                WSData.log_interaction("show_my_profile");
            }
            else {
                $("#my_profile_arrow").attr('class', 'fa fa-chevron-down');
                $("#my_profile").attr('aria-hidden', 'true');

                setTimeout(function() {
                    $("#toggle_my_profile").attr("title", $("#profile_toggle_hidden").text());
                    $("#my_profile_arrow").attr('class', 'fa fa-chevron-down');
                    $("#my_profile").hide();
                }, 900);
            }
        });
    },

};
