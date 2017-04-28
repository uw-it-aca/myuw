var Profile = {
    render_upon_data: function() {
        var source = $("#profile-content").html();
        var template = Handlebars.compile(source);

        // Process data to determine if there are any pending majors or minors
        var profile_data = WSData.profile_data();

        if(profile_data.term_majors && profile_data.term_majors.length > 0){
            for(var i = 0; i < profile_data.term_majors.length; i++){
                if(!profile_data.term_majors[i].same_as_previous){
                    profile_data.has_pending_major = true;
                }
            }

            if(!profile_data.hasOwnProperty('has_pending_major'))
                profile_data.has_pending_major = false;
        }


        if(profile_data.term_minors && profile_data.term_minors.length > 0){
            for(var e = 0; e < profile_data.term_minors.length; e++){
                if(!profile_data.term_minors[e].same_as_previous){
                    profile_data.has_pending_minor = true;
                }
            }

            if(!profile_data.hasOwnProperty('has_pending_minor'))
                profile_data.has_pending_minor = false;
        }

        $("#profile").html(template(WSData.profile_data()));
        $("#toggle_my_profile").attr("title", $("#profile_toggle_hidden").text());
        $("#toggle_my_profile").attr("aria-label", $("#profile_toggle_hidden").text());
        Profile.add_events();
    },

    add_events: function() {
        $("#toggle_my_profile").on("click", function(ev) {
            ev.preventDefault();
            var my_profile = $("#my_profile");
            if (my_profile.css('display') == 'none') {
                my_profile.show();
                // Without this timeout, the animation doesn't happen - the block just appears.
                setTimeout(function() {
                    $("#my_profile").toggleClass("slide-show");
                    $("#my_profile_arrow").attr('class', 'fa fa-chevron-up');
                    my_profile.attr('aria-hidden', 'false');
                    $("#toggle_my_profile").attr("title", $("#profile_toggle_displayed").text());
                    $("#toggle_my_profile").attr("aria-label", $("#profile_toggle_displayed").text());
                    WSData.log_interaction("show_my_profile");
                }, 0);
            }
            else {
                my_profile.toggleClass("slide-show");
                $("#my_profile_arrow").attr('class', 'fa fa-chevron-down');
                my_profile.attr('aria-hidden', 'true');

                setTimeout(function() {
                    $("#toggle_my_profile").attr("title", $("#profile_toggle_hidden").text());
                    $("#toggle_my_profile").attr("aria-label", $("#profile_toggle_hidden").text());
                    $("#my_profile_arrow").attr('class', 'fa fa-chevron-down');
                    $("#my_profile").hide();
                }, 900);
            }
        });
    },

};
