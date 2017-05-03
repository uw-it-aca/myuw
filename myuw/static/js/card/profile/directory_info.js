var DirectoryInfoCard = {
    name: 'DirectoryInfoCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_profile_data(DirectoryInfoCard.render_upon_data, DirectoryInfoCard.render_error);
    },

    render_upon_data: function () {
        if (!DirectoryInfoCard._has_all_data()) {
            return;
        }
        DirectoryInfoCard._render();
    },

    _render: function () {
        var directory_info = WSData.profile_data();
        var source = $("#directory_info_card").html();
        var template = Handlebars.compile(source);
        DirectoryInfoCard.dom_target.html(template(directory_info));
        LogUtils.cardLoaded(DirectoryInfoCard.name, DirectoryInfoCard.dom_target);
    },

    _has_all_data: function () {
        if (WSData.profile_data()) {
            return true;
        }
        return false;
    },

    render_error: function () {
        $("#DirectoryInfoCard").hide();
    }
};
