var LibraryCard = {
    name: 'LibraryCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_library_data(LibraryCard.render_upon_data,
                                  LibraryCard.show_error);
    },

    render_upon_data: function() {
        if (!LibraryCard._has_all_data()) {
            return;
        }
        LibraryCard._render(WSData.library_data());
    },

    _render: function (library_data) {
        var source = $("#library_card_content").html();
        var template = Handlebars.compile(source);
        LibraryCard.dom_target.html(template(library_data));
        LogUtils.cardLoaded(LibraryCard.name, LibraryCard.dom_target);
    },

    _has_all_data: function () {
        if (WSData.library_data()) {
            return true;
        }
        return false;
    },

    show_error: function(status) {
        if (status === 404) {
            LibraryCard._render({"holds_ready": 0, "items_loaned": 0});
            return;
        }
        var raw = CardWithError.render("Library Account");
        LibraryCard.dom_target.html(raw);
    }

};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.LibraryCard = LibraryCard;
