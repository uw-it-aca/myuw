var Category = {
    show_category_page: function(category) {
        UwEmail.render_init();
        WSData.fetch_category_links(Category.render_category_page, undefined, [category]);
    },

    render_category_page: function(category) {
        data = WSData.category_link_data(category);
        document.title = data.category_name;
        source = $("#category_page").html();
        template = Handlebars.compile(source);

        $("#main-content").html(template(data));
    }
};
