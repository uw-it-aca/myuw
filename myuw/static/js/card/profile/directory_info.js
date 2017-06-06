var DirectoryInfoCard = {
    name: 'DirectoryInfoCard',
    dom_target: undefined,

    render_init: function() {
        if (myuwFeatureEnabled('employee_profile') && 
            (window.user.employee || window.user.faculty || window.user.stud_employee)) {
            WSData.fetch_directory_data(DirectoryInfoCard.render_upon_data, DirectoryInfoCard.render_error);
        } else {
            $("#DirectoryInfoCard").hide();
            return;
        }
    },

    render_upon_data: function () {
        if (!DirectoryInfoCard._has_all_data()) {
            return;
        }
        DirectoryInfoCard._render();
    },

    _render: function () {
        var directory_info = WSData.directory_data();
        var source = $("#directory_info_card").html();
        var template = Handlebars.compile(source);

        // enhanced directory info
        directory_info.is_tacoma = window.user.tacoma;

        DirectoryInfoCard.dom_target.html(template(directory_info));
        LogUtils.cardLoaded(DirectoryInfoCard.name, DirectoryInfoCard.dom_target);
    },

    _has_all_data: function () {
        if (WSData.directory_data()) {
            return true;
        }
        return false;
    },

    render_error: function () {
        $("#DirectoryInfoCard").hide();
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.DirectoryInfoCard = DirectoryInfoCard;
