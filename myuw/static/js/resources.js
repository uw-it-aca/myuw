var Resources = {

    render: function() {
        showLoading();
        Resources.load_resource_data();
    },

    make_html: function () {
        if (WSData.resource_data()) {
            Handlebars.registerPartial('resource_content', $("#resource_content").html());
            var resource_data = WSData.resource_data();
            $('html,body').animate({scrollTop: 0}, 'fast');
            var source = $("#resource_page").html();
            var template = Handlebars.compile(source);
            var content = template({'categories': resource_data});
            $("#main-content").html(content);
        }

    },

    load_resource_data: function () {
        WSData.fetch_resource_data(Resources.make_html,
            Resources.resource_error);

    },

    render_cards: function () {
        if (WSData.resource_data()) {
            var resource_data = WSData.resource_data();
            $(resource_data).each(function(idx, category){
                console.log(category.category_name);
            });
            var card = ResourcesCard;
            card.dom_target = $("#explore_cards");
        }

    },

    resource_error: function () {
        console.log('err');
    }

};
