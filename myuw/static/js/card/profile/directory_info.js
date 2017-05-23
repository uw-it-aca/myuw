var DirectoryInfoCard = {
    name: 'DirectoryInfoCard',
    dom_target: undefined,

    render_init: function() {
        if (myuwFeatureEnabled('employee_profile') && 
            (window.user.employee || window.user.faculty || window.user.stud_employee)) {
            WebServiceData.require({directory_data: new DirectoryData()},
                                   DirectoryInfoCard.render);
        } else {
            $("#DirectoryInfoCard").hide();
        }
    },

    render: function (resources) {
        var directory_resource = resources.directory_data;

        if (DirectoryInfoCard.render_error(directory_resource.error)) {
            return;
        }

        var directory_info = directory_resource.data;
        var source = $("#directory_info_card").html();
        var template = Handlebars.compile(source);
        DirectoryInfoCard.dom_target.html(template(directory_info));
        LogUtils.cardLoaded(DirectoryInfoCard.name, DirectoryInfoCard.dom_target);
    },

    render_error: function (directory_resource_error) {
        if (directory_resource_error) {
            $("#DirectoryInfoCard").hide();
            return true;
        }

        return false;
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.DirectoryInfoCard = DirectoryInfoCard;
