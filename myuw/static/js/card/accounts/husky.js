var HuskyCard = {
    name: 'HuskyCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_hfs_data(HuskyCard.render_upon_data,
                              HuskyCard.render_error);
    },

    render_upon_data: function () {
        if (!HuskyCard._has_all_data()) {
            return;
        }
        HuskyCard._render();
    },

    _render_with_context: function(context){
        var source = $("#husky_card_content").html();
        var template = Handlebars.compile(source);
        HuskyCard.dom_target.html(template(context));
    },

    _render: function () {
        var hfs_data = WSData.hfs_data();
        hfs_data.is_tacoma = window.user.tacoma_affil || window.user.tacoma;
        if (!hfs_data.student_husky_card &&
            !hfs_data.employee_husky_card) {
            remove_card(HuskyCard.dom_target);
        } else {
            HuskyCard._render_with_context(hfs_data);
            LogUtils.cardLoaded(HuskyCard.name, HuskyCard.dom_target);
        }
    },

    _has_all_data: function () {
        if (WSData.hfs_data()) {
            return true;
        }
        return false;
    },

    render_error: function (status) {
        if (status === 404) {
            remove_card(HuskyCard.dom_target);
            return;
        }
        HuskyCard._render_with_context({has_error: true});
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.HuskyCard = HuskyCard;
