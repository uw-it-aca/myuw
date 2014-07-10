var TextbookCard = {
    name: 'TextbookCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_book_data(TextbookCard.render_upon_data);
    },

    render_upon_data: function() {
        //If more than one data source, multiple callbacks point to this function
        //Delay rendering until all requests are complete
        //Do something smart about not showing error if AJAX is pending
        if (!TextbookCard._has_all_data()) {
            TextbookCard.dom_target.html(CardWithError.render());
            return;
        }
        TextbookCard._render();
    },

    _render: function () {
        var source = $("#textbook_card").html();
        var template = Handlebars.compile(source);
        TextbookCard.dom_target.html(template());
    },

    _has_all_data: function () {
        if (WSData.book_data()) {
            return true;
        }
        return false;
    }

};
