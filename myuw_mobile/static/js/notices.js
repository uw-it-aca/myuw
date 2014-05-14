/*global $, Handlebars, WSData*/

var Notices = {
    show_notices: function () {
        "use strict";
        WSData.fetch_notice_data(Notices.render_notices);
    },

    render_notices: function () {
        "use strict";
        var notices, source, template,
            expanded = false;
        notices = WSData.notice_data();

        source = $("#notices").html();
        template = Handlebars.compile(source);
        $("#main-content").html(template(notices));
        /* Events for expand/close all */
        $(".disclosure_toggle").click(function () {
            if (expanded) {
                expanded = false;
                $(".panel-collapse").collapse("hide");
                $("#expand").show();
                $("#collapse").hide();
            }
            else if (!expanded) {
                expanded = true;
                $(".panel-collapse").collapse("show");
                $("#expand").hide();
                $("#collapse").show();
            }

        });

    }
};
