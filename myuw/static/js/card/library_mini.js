var LibraryCardMini = {
    name: 'LibraryCardMini',
    dom_target: undefined,

    render_init: function() {
        debugger
        WebServiceData.require({library_data: new LibraryData()}, LibraryCardMini.render);
    },

    render: function (resources) {
        var library_data_resource = resources.library_data;
        if (LibraryCardMini.show_error(library_data_resource.error)) {
            return;
        }

        var library_data = library_data_resource.data;
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

    show_error: function(library_resource_error) {
        if (library_resource_error) {
            var status = library_resource_error.status;
            if (status === 404) {
                LibraryCardMini.dom_target.hide();
            } else {
                var raw = CardWithError.render("Library Account");
                LibraryCardMini.dom_target.html(raw);
            }

            return true;
        }

        return false;
    }
};
