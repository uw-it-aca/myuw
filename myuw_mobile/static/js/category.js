var Category = {
    show_category_page: function() {
        source = $("#category_page").html();
        template = Handlebars.compile(source);

        $("#main-content").html(template());
    }
};
