var RequestEmailLists = {
    render: function() {
        var source   = $("#request_email_lists_tmpl").html();
        var template = Handlebars.compile(source);
        var raw = template({});
        return raw;
    }
};
