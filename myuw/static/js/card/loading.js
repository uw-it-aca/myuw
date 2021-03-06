var CardLoading = {
    render: function( card_name_str ) {
        var source   = $("#card_is_loading").html();
        var template = Handlebars.compile(source);
        return template({card_name: card_name_str});
    },
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.CardLoading = CardLoading;
