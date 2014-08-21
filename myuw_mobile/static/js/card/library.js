var LibraryCard = {
    name: 'LibraryCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_library_data(LibraryCard.render_upon_data, LibraryCard.show_error);
    },

    render_upon_data: function() {
        //If more than one data source, multiple callbacks point to this function
        //Delay rendering until all requests are complete
        //Do something smart about not showing error if AJAX is pending
        if (!LibraryCard._has_all_data()) {
            LibraryCard.dom_target.html(CardWithError.render());
            return;
        }
        LibraryCard._render(WSData.library_data());
    },

    _render: function (library_data) {
        var source = $("#library_card_content").html();
        var template = Handlebars.compile(source);
        if (!library_data.next_due && !library_data.holds_ready && !library_data.items_loaned && !library_data.fines) {
            library_data = null;
        }
        LibraryCard.dom_target.html(template({mylibaccount: library_data}));
    },

    _has_all_data: function () {
        if (WSData.library_data()) {
            return true;
        }
        return false;
    },

    show_error: function() {
        LibraryCard.dom_target.html(CardWithError.render("Library Account"));
    }

};
