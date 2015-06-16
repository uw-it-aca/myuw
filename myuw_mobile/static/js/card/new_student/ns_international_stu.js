var InternationalStuCard = {
    name: 'InternationalStuCard',
    dom_target: undefined,
    render_init: function() {
        InternationalStuCard.dom_target.html(InternationalStuCard.render());
    },

    render: function () {
        var source = $("#ns_international_stu").html();
        var template = Handlebars.compile(source);
        return template({});
    },
};
