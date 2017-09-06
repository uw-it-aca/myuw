var OutageCard = {
    name: 'OutageCard',
    term: 'current',
    dom_target: undefined,
    rendered_once: false,

    hide_card: function() {
        if (window.user.student ||
            window.user.instructor ||
            window.user.employee) {
            return false;
        }
        return true;
    },


    render_init: function() {
        if (OutageCard.hide_card()) {
            $("#OutageCard").hide();
            return;
        }
        if (window.user.student) {
            WSData.fetch_course_data_for_term(OutageCard.term,
                                              OutageCard.render,
                                              OutageCard.render);
            WSData.fetch_notice_data(OutageCard.render,
                                     OutageCard.render);
            WSData.fetch_profile_data(OutageCard.render,
                                      OutageCard.render);
        }
        if (window.user.instructor) {
            WSData.fetch_instructed_course_data_for_term(window.term.display_term,
                                                         OutageCard.render,
                                                         OutageCard.render);
        }
        if (window.user.employee) {
            WSData.fetch_directory_data(OutageCard.render,
                                        OutageCard.render);
        }
    },

    render: function () {
        if (window.user.student) {
            var notices = WSData._notice_data;
            var notice_err = WSData._notice_error_status;
            var profile = WSData.profile_data();
            var profile_err = WSData._profile_error_status;
            var course_data = WSData._course_data[OutageCard.term];
            var course_err = WSData.course_data_error_code(OutageCard.term);
            if ((profile || profile_err === 404) &&
                (course_data || course_err === 404) &&
                (notices || notice_err === 404)) {
            } else if (profile_err && profile_err !== 404 ||
                       course_err && course_err !== 404 ||
                       notice_err && notice_err !== 404) {
                OutageCard.render_error();
                return;
            } else {
                return;
            }
        }
        if (window.user.instructor) {
            var instructor_course = WSData._instructed_course_data[window.term.display_term];
            var instructor_course_err = WSData.instructed_course_data_error_code(window.term.display_term);
            if (instructor_course || instructor_course_err === 404) {
            } else if (instructor_course_err &&
                       instructor_course_err !== 404) {
                OutageCard.render_error();
                return;
            } else {
                return;
            }
        }
        if (window.user.employee) {
            var dir_info = WSData.directory_data();
            var dir_info_err = WSData._directory_error_status;
            if (dir_info || dir_info_err === 404) {
            } else if (dir_info_err && dir_info_err !== 404) {
                OutageCard.render_error();
                return;
            } else {
                return;
            }
        }

        $("#OutageCard").hide();
    },

    render_error: function () {
        if (OutageCard.rendered_once) {
            return;
        }
        var source = $("#outage_card_content").html();
        var template = Handlebars.compile(source);

        OutageCard.dom_target.html(template());
        LogUtils.cardLoaded(OutageCard.name, OutageCard.dom_target);
        OutageCard.rendered_once = true;
   },

    reset: function() {
        OutageCard.rendered_once = false;
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.OutageCard = OutageCard;
