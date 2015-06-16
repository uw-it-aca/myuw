var SummerEFSCard = {
    name: 'SummerEFSCard',
    dom_target: undefined,
    render_init: function() {
        SummerEFSCard.dom_target.html(SummerEFSCard.render());
    },

    render: function () {
        var source = $("#ns_summer_efs").html();
        var template = Handlebars.compile(source);
        return template({});
    },
};
