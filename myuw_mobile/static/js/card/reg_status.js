var RegStatusCard = {
    name: 'RegStatusCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_notice_data(RegStatusCard.render_upon_data);
    },
    render_upon_data: function() {
        //If more than one data source, multiple callbacks point to this function
        //Delay rendering until all requests are complete
        //Do something smart about not showing error if AJAX is pending
        if (!RegStatusCard._has_all_data()) {
            RegStatusCard.dom_target.html(CardWithError.render());
            return;
        }
        RegStatusCard._render();
    },

    _has_all_data: function () {
        if (WSData.notice_data()) {
            return true;
        }
        return false;
    },

    _render: function () {
        var source = $("#reg_status_card").html();
        var template = Handlebars.compile(source);
        var reg_notices = Notices.get_notices_for_tag("reg_card_messages");

        // show registration resources
        $('body').on('click', '#show_reg_resources', function (ev) {

            ev.preventDefault();

            $("#reg_resources").toggleClass("slide-show");

            if ($("#reg_resources").hasClass("slide-show")) {
                $("#show_reg_resources").text("Show less")
                $("#reg_resources").attr('aria-hidden', 'false');
                $("#show_reg_resources").attr('title', 'Collapse to hide additional registration resources');
            } else {

                $("#reg_resources").attr('aria-hidden', 'true');
                $("#show_reg_resources").attr('title', 'Expand to show additional registration resources');

                setTimeout(function() {
                    $("#show_reg_resources").text("Show more");
                }, 700);
            }
        });

        // show hold details
        $('body').on('click', '#show_reg_holds', function (ev) {

            ev.preventDefault();

            $("#reg_holds").toggleClass("slide-show");

            if ($("#reg_holds").hasClass("slide-show")) {

                $("#show_reg_holds").text("Hide holds")
                $("#reg_holds").attr('aria-hidden', 'false');
                $("#show_reg_holds").attr('title', 'Collapse to hide holds information');
            }
            else {
                $("#reg_holds").attr('aria-hidden', 'true');
                $("#show_reg_holds").attr('title', 'Expand to show holds information');

                setTimeout(function() {
                    /* TODO: need to get a value for holds count */
                    $("#show_reg_holds").text("Show 333 Holds");
                }, 700);
            }
        });

        RegStatusCard.dom_target.html(template({"reg_notices": reg_notices,
                                                "is_tacoma": window.user.tacoma,
                                                "is_bothell": window.user.bothell,
                                                "is_seattle": window.user.seattle}));
    }
};
