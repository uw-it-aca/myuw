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
        var reg_notices = Notices.get_notices_for_category("Registration");

        // show registration resources
        $('body').on('click', '#show_reg_resources', function (ev) {

            ev.preventDefault();

            $("#reg_resources").toggleClass("slide-show");

            if ($("#reg_resources").hasClass("slide-show")) {
               $("#show_reg_resources").text("Show less...")
               $("#reg_resources").attr('aria-hidden', 'false');
            }
            else {
               $("#show_reg_resources").text("Show more...");
               $("#reg_resources").attr('aria-hidden', 'true');
            }

        });

        // show hold details
        $('body').on('click', '#show_reg_holds', function (ev) {

            ev.preventDefault();

            $("#reg_holds").toggleClass("slide-show");

            if ($("#reg_holds").hasClass("slide-show")) {
               $("#show_reg_holds").text("Hide details")
               $("#reg_holds").attr('aria-hidden', 'false');
            }
            else {
               $("#show_reg_holds").text("Show details");
               $("#reg_holds").attr('aria-hidden', 'true');
            }

        });

        RegStatusCard.dom_target.html(template({"reg_notices": reg_notices}));
    }
};
