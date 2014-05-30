var LibraryCard = {
    render: function (lib_notices) {
        var source = $("#library_card").html();
        var template = Handlebars.compile(source);
        return template({'mylibaccount': WSData.library_data()});
    },

};
