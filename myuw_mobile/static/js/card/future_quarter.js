var FutureQuarterCard = {
    name: 'FutureQuarterCard',
    dom_target: undefined,

    render_init: function() {
        // TODO Fetch real data
        FutureQuarterCard._render()
    },

    render_upon_data: function() {
        //If more than one data source, multiple callbacks point to this function
        //Delay rendering until all requests are complete
        //Do something smart about not showing error if AJAX is pending
        if (!FutureQuarterCard._has_all_data()) {
            FutureQuarterCard.dom_target.html(CardWithError.render());
            return;
        }

    },

    _render: function () {
        var source = $("#future_quarter_card").html();
        var template = Handlebars.compile(source);
        FutureQuarterCard.dom_target.html(template());
    },

    _has_all_data: function () {
        //TODO Update to use real data
        if (true) {
            return true;
        }
        return false;
    }

};
