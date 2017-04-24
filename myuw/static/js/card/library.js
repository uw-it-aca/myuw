var LibraryCard = {
    name: 'LibraryCard',
    dom_target: undefined,

    render_init: function() {
        WebServiceData.require({library_data: new LibraryData()}, LibraryCard.render);
    },

    render: function (resources) {
        if (LibraryCard.show_error(resources.library_data.error)) {
            return;
        }

        var source = $("#library_card_content").html();
        var template = Handlebars.compile(source);
        var library_data = resources.library_data.data;

        if (!library_data.next_due && !library_data.holds_ready && !library_data.items_loaned && !library_data.fines) {
            LibraryCard.dom_target.hide();
        }
        else {
            LibraryCard.dom_target.html(template(library_data));
            LogUtils.cardLoaded(LibraryCard.name, LibraryCard.dom_target);
        }
    },

    show_error: function(library_resource_error) {
        if (library_resource_error) {
            if (library_resource_error.status === 404) {
                LibraryCard.dom_target.hide();
            } else {
                var raw = CardWithError.render("Library Account");
                LibraryCard.dom_target.html(raw);
            }

            return true;
        }

        return false;
    }

};
