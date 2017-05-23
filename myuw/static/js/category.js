var Category = {
    show_category_page: function(category, topic) {
        //Navbar.render_navbar("nav-sub");
        CommonLoading.render_init();
        WebServiceData.require({category_links: new CategoryLinkData(category)},
                               Category.render_category_page, [category, topic]);
    },

    render_category_page: function(category, topic, resources) {
        if (Category.render_error(resources.category_links.error)) {
            return;
        }

        var data = resources.category_links.data;
        var title = document.title.replace("Category", data.category_name);

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

    render_error: function(category_error) {
        if (category_error) {
            console.log('category_err: ' + category_error.status);
            return true;
        }

        return false;
    }
};
