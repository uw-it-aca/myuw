var ContentError = {

    render: function(page_name) {
        var source = $("#page_content_error").html();
        var template = Handlebars.compile(source);
        var raw = template({"page_name": page_name});
        $("#main-content").html(raw);
    }
};
