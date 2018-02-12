var HfsSeaCard = {
    name: 'HfsSeaCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_hfs_data(HfsSeaCard.render_upon_data,
                              HfsSeaCard.render_error);
    },

    render_upon_data: function () {
        if (!HfsSeaCard._has_all_data()) {
            return;
        }
        HfsSeaCard._render();
    },

    _render: function () {
        var hfs_data = WSData.hfs_data();
        var source = $("#sea_hfs_card").html();
        var template = Handlebars.compile(source);
        var template_data;
        if (!hfs_data.resident_dining) {
            remove_card(HfsSeaCard.dom_target);
        } else {
            HfsSeaCard.dom_target.html(template(hfs_data));
            LogUtils.cardLoaded(HfsSeaCard.name, HfsSeaCard.dom_target);
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
            remove_card(HfsSeaCard.dom_target);
            return;
        }
        var raw = CardWithError.render("HFS Card");
        HfsSeaCard.dom_target.html(raw);
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.HfsSeaCard = HfsSeaCard;
