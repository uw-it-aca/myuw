var Profile = {
    render_upon_data: function() {
        var source = $("#profile-content").html();
        var template = Handlebars.compile(source);
        $("#my_profile").html(template(WSData.profile_data()));
    },

    add_events: function() {
        $("#toggle_my_profile").on("click", function(ev) {
            ev.preventDefault();
            $("#my_profile").toggleClass("slide-show");

            if ($("#my_profile").hasClass("slide-show")) {
                $("#my_profile_arrow").attr('class', 'fa fa-chevron-up');
                $("#my_profile").attr('aria-hidden', 'false');
                WSData.log_interaction("show_my_profile");
            }
            else {
                $("#my_profile_arrow").attr('class', 'fa fa-chevron-down');
                $("#my_profile").attr('aria-hidden', 'true');

                setTimeout(function() {
                    $("#my_profile_arrow").attr('class', 'fa fa-chevron-down');
                }, 900);
            }
        });
    },

};
