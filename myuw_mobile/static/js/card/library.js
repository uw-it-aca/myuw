var LibraryCard = {
    render: function () {
        var source = $("#library_card_content").html();
        var template = Handlebars.compile(source);
        return template({mylibaccount: WSData.library_data()});
    },

    render_init: function() {
        if (!WSData.library_data()) {
            return CardLoading.render("Library");
        }
        return LibraryCard.render();
    },

    render_upon_data: function() {
        var html_content = LibraryCard.render();
        $("#library_card_row").html(html_content);
    },

};
