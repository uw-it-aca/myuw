var CriticalInfoCard = {
    name: 'CriticalInfoCard',
    dom_target: undefined,
    render_init: function() {
        CriticalInfoCard.dom_target.html(CriticalInfoCard.render());
    },

    render: function () {
        var source = $("#ns_critical_info").html();
        var template = Handlebars.compile(source);
        return template({});
    },
};
