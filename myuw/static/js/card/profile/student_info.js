var StudentInfoCard = {
    name: 'StudentInfoCard',
    dom_target: undefined,

    render_init: function() {
        if (window.user.student || window.user.stud_employee) {
            debugger
            WebServiceData.require({profile_data: new ProfileData()}, StudentInfoCard.render);
        } else {
            $("#StudentInfoCard").hide();
            return;
        }
    },

    render: function (resources) {
        var profile_data_resource = resources.profile_data;

        if (StudentInfoCard.render_error(profile_data_resource.error)) {
            return;
        }

        var student_info = profile_data_resource.data;
        var source = $("#student_info_card").html();
        var template = Handlebars.compile(source);

        StudentInfoCard.dom_target.html(template(student_info));
        LogUtils.cardLoaded(StudentInfoCard.name, StudentInfoCard.dom_target);
    },

    render_error: function (profile_resource_error) {
        if (profile_resource_error) {
            $("#StudentInfoCard").hide();
            return true;
        }

        return false;
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.StudentInfoCard = StudentInfoCard;
