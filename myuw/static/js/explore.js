var Explore = {

    render: function() {
        showLoading();
        Explore.load_explore_data();
    },

    make_html: function () {
        if (WSData.explore_data()) {
            var explore_data = WSData.explore_data();
            $('html,body').animate({scrollTop: 0}, 'fast');
            var source = $("#explore_page").html();
            var template = Handlebars.compile(source);
            var content = template({'categories': explore_data});
            $("#main-content").html(content);
        }

    },

    load_explore_data: function () {
        WSData.fetch_explore_data(Explore.make_html,
            Explore.explore_error);

    },

    render_cards: function () {
        if (WSData.explore_data()) {
            var explore_data = WSData.explore_data();
            $(explore_data).each(function(idx, category){
                console.log(category.category_name);
            });
            var card = ExploreCard;
            card.dom_target = $("#explore_cards");
        }

    },

    explore_error: function () {
        console.log('err');
    }

};
