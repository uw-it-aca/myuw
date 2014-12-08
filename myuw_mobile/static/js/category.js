var Category = {
    show_category_page: function(category, topic) {
        //Navbar.render_navbar("nav-sub");
        CommonLoading.render_init();
        WSData.fetch_category_links(Category.render_category_page, Category.render_error, [category, topic]);
    },

    render_category_page: function(category, topic) {
        var data = WSData.category_link_data(category);

        var title = window.page_titles.category_page.replace("Category", data.category_name);

        document.title = title;
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
