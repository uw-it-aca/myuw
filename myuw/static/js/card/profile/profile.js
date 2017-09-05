var CommonProfileCard = {
    name: 'CommonProfileCard',
    dom_target: undefined,

    hide_card: function() {
        if (window.user.employee) {
            return false;
        }
        return true;
    },


    render_init: function() {
        if (CommonProfileCard.hide_card()) {
            $("#CommonProfileCard").hide();
            return;
        }
        WSData.fetch_directory_data(CommonProfileCard.render_upon_data);
    },

    render_upon_data: function () {
        if (WSData.directory_data()) {
            CommonProfileCard._render();
            return;
        }
        var dir_info_err = WSData._directory_error_status;
        if (dir_info_err === 404) {
            $("#CommonProfileCard").hide();
            return;
        }
        var raw = CardWithError.render("Profile Card");
        CommonProfileCard.dom_target.html(raw);
    },

    _has_all_data: function () {
            return true;
        }
        return false;
    },

    _render: function() {
        var directory_data = WSData.directory_data();
        var source   = $("#common_profile_card").html();
        var template = Handlebars.compile(source);
        directory_data.card_name = CommonProfileCard.name;
        var compiled = template({
            display_name: directory_data.display_name,
            full_name: directory_data.full_name,
            has_preferred: (directory_data.display_name !== directory_data.full_name)
        });
        CommonProfileCard.dom_target.html(compiled);
    }
};
