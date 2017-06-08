var LibraryCardMini = {
    name: 'LibraryCardMini',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_library_data(LibraryCardMini.render_upon_data, LibraryCardMini.show_error);
    },

    render_upon_data: function() {
        //If more than one data source, multiple callbacks point to this function
        //Delay rendering until all requests are complete
        //Do something smart about not showing error if AJAX is pending
        if (!LibraryCardMini._has_all_data()) {
            return;
        }
        LibraryCardMini._render(WSData.library_data());
    },

    _render: function (library_data) {
        var source = $("#library_card_mini_content").html();
        var template = Handlebars.compile(source);
        if (!library_data.next_due && !library_data.holds_ready && !library_data.items_loaned && !library_data.fines) {
            LibraryCardMini.dom_target.hide();
        }
        else {
            LibraryCardMini.dom_target.html(template(library_data));
            LogUtils.cardLoaded(LibraryCardMini.name, LibraryCardMini.dom_target);
        }
    },

    _has_all_data: function () {
        if (WSData.library_data()) {
            return true;
        }
        return false;
    },

    show_error: function(status) {
        if (status === 404) {
            LibraryCardMini.dom_target.hide();
            return;
        }
        var raw = CardWithError.render("Library Account");
        LibraryCardMini.dom_target.html(raw);
    }

};
