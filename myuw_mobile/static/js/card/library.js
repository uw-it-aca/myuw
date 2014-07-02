var LibraryCard = {

    render_init: function() {
        var library_data = WSData.library_data()
        if (!library_data) {
            $("#library_card_row").html(CardLoading.render("Library"));
            return;
        }
        LibraryCard.render(library_data);
    },

    render_upon_data: function() {
        var library_data = WSData.library_data()
        if (!library_data) {
            $("#library_card_row").html(CardWithError.render());
            return;
        }
        LibraryCard.render(library_data);
    },

    render: function (library_data) {
        var source = $("#library_card_content").html();
        var template = Handlebars.compile(source);
        $("#library_card_row").html(template({mylibaccount: library_data}));
    },

};
