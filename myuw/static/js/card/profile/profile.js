var CommonProfileCard = {
    name: 'CommonProfileCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_directory_data(CommonProfileCard.render_upon_data,
                                    CommonProfileCard.render_upon_data);
    },

    render_upon_data: function () {
        if (WSData.directory_data()) {
            CommonProfileCard._render();
            return;
        }
        $("#CommonProfileCard").hide();
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

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.CommonProfileCard = CommonProfileCard;
