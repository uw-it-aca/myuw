var Category = {
    show_category_page: function(category, topic) {
        Navbar.render_navbar();
        UwEmail.render_init();
        WSData.fetch_category_links(Category.render_category_page, Category.render_error, [category, topic]);
    },

    render_category_page: function(category, topic) {
        data = WSData.category_link_data(category);
        document.title = data.category_name;
        source = $("#category_page").html();
        template = Handlebars.compile(source);

        $("#main-content").html(template(data));
        //Scroll to subucategory
        element = $("#" + topic);
        if (element.length > 0) {
                $('html, body').animate({
                scrollTop: element.offset().top
            });
        }
    },

    render_error: function() {
        console.log('err');
    }
};
