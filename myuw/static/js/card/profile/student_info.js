var StudentInfoCard = {
    name: 'StudentInfoCard',
    dom_target: undefined,

    render_init: function() {
        if (window.user.student || window.user.stud_employee) {
            WSData.fetch_profile_data(StudentInfoCard.render_upon_data, StudentInfoCard.render_error);
        } else {
            $("#StudentInfoCard").hide();
            return;
        }
    },

    render_upon_data: function () {
        if (!StudentInfoCard._has_all_data()) {
            return;
        }
        StudentInfoCard._render();
    },

    _render: function () {
        var student_info = WSData.profile_data();
        var source = $("#student_info_card").html();
        var template = Handlebars.compile(source);

        StudentInfoCard.dom_target.html(template(student_info));
        LogUtils.cardLoaded(StudentInfoCard.name, StudentInfoCard.dom_target);
    },

    _has_all_data: function () {
        if (WSData.profile_data()) {
            return true;
        }
        return false;
    },

    render_error: function () {
        $("#StudentInfoCard").hide();
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.StudentInfoCard = StudentInfoCard;
