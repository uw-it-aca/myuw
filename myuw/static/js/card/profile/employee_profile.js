var EmployeeInfoCard = {
    name: 'EmployeeInfoCard',
    dom_target: undefined,

    hide_card: function() {
        if (window.user.employee || window.user.stud_employee) {
            return false;
        }
        return true;
    },

    render_init: function() {
        if (EmployeeInfoCard.hide_card()) {
            $("#EmployeeInfoCard").hide();
            return;
        }
        WSData.fetch_directory_data(EmployeeInfoCard.render_upon_data,
                                    EmployeeInfoCard.render_error);
    },

    render_upon_data: function () {
        if (WSData.directory_data()) {
            EmployeeInfoCard._render();
        }
    },

    _render: function () {
        var directory_info = WSData.directory_data();
        var source = $("#directory_info_card").html();
        var template = Handlebars.compile(source);

        // enhanced directory info
        directory_info.is_tacoma = window.user.tacoma;

        EmployeeInfoCard.dom_target.html(template(directory_info));
        LogUtils.cardLoaded(EmployeeInfoCard.name, EmployeeInfoCard.dom_target);
    },

    render_error: function () {
        $("#EmployeeInfoCard").hide();
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.EmployeeInfoCard = EmployeeInfoCard;
