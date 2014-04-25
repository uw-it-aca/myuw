/*global $, Handlebars, WSData*/

var Notices = {
    show_notices: function () {
        "use strict";
        WSData.fetch_notice_data(Notices.render_notices);
    },

    render_notices: function () {
        "use strict";
        var notices, source, template;
        notices = WSData.notice_data();

        source = $("#notices").html();
        template = Handlebars.compile(source);
        $("#courselist").html(template(notices));
    }
};
