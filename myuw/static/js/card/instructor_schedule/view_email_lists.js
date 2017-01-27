var ViewEmailLists = {
    render: function() {
        var source   = $("#view_email_lists_tmpl").html();
        var template = Handlebars.compile(source);
        var raw = template({});
        return raw;
    }
};
