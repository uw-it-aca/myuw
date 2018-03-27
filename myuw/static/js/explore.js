var Explore = {

    render: function() {
        showLoading();
        Explore.make_html();
    },

    make_html: function () {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var source = $("#explore_page").html();
        var template = Handlebars.compile(source);
        var content = template({});
        $("#main-content").html(content);
        Explore.load_all_cards();
    },

    load_all_cards: function () {
        WSData.fetch_explore_data(Explore.render_cards,
                                  Explore.explore_error);

    },

    render_cards: function () {
        if (WSData.explore_data()) {
            var explore_data = WSData.explore_data();
            $(explore_data).each(function(idx, category){
                console.log(category);
            });
            var card = ExploreCard;
            card.dom_target = $("#explore_cards");
        }

    },

    explore_error: function () {
        console.log('err');
    }

};
