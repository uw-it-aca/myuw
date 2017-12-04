var DirectoryInfoCard = {
    name: 'DirectoryInfoCard',
    dom_target: undefined,

    hide_card: function() {
        if (window.user.employee) {
            return false;
        }
        return true;
    },

    render_init: function() {
        if (DirectoryInfoCard.hide_card()) {
            $("#DirectoryInfoCard").hide();
            return;
        }
        WSData.fetch_directory_data(DirectoryInfoCard.render_upon_data,
                                    DirectoryInfoCard.render_error);
    },

    render_upon_data: function () {
        if (WSData.directory_data()) {
            DirectoryInfoCard._render();
        }
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

    render_error: function () {
        $("#DirectoryInfoCard").hide();
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.DirectoryInfoCard = DirectoryInfoCard;
