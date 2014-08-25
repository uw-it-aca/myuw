var RegStatusCard = {
    name: 'RegStatusCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_notice_data(RegStatusCard.render_upon_data,RegStatusCard.render_error);
    },
    render_upon_data: function() {
        //If more than one data source, multiple callbacks point to this function
        //Delay rendering until all requests are complete
        //Do something smart about not showing error if AJAX is pending
        if (!RegStatusCard._has_all_data()) {
            RegStatusCard.render_error();
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
    render_error: function () {1779
        RegStatusCard.dom_target.html(CardWithError.render("Registration"));
    },

    _render: function () {
        var source = $("#reg_status_card").html();
        var template = Handlebars.compile(source);
        var reg_notices = Notices.get_notices_for_tag("reg_card_messages");
        var reg_holds = Notices.get_notices_for_tag("reg_card_holds");
        var reg_date = Notices.get_notices_for_tag("est_reg_date");

        //Get hold count from notice attrs
        var hold_count = 0;
        $.each(reg_holds, function(idx, notice) {
            $.each(notice['attributes'], function(idx, attribute){
                if (attribute['name'] === "Holds") {
                    hold_count = attribute['value'];
                }
            });
        });

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
        $("#show_reg_holds").text("Show " + hold_count + " holds");
        $('body').on('click', '.reg_disclosure', function (ev) {
            ev.preventDefault();

            $("#reg_holds").toggleClass("slide-show");
            if ($("#reg_holds").hasClass("slide-show")) {
                $("#show_reg_holds").hide();
                $("#hide_reg_holds").show();
            }
            else {
                setTimeout(function () {
                    $("#show_reg_holds").show();
                    $("#hide_reg_holds").hide();
                }, 700);
            }
        });

        RegStatusCard.dom_target.html(template({"reg_notices": reg_notices,
                                                "reg_holds": reg_holds,
                                                "is_tacoma": window.user.tacoma,
                                                "is_bothell": window.user.bothell,
                                                "is_seattle": window.user.seattle,
                                                "hold_count": hold_count,
                                                "est_reg_date": reg_date}));
    }
};
