var ProfileCard = {
    name: 'ProfileCard',
    dom_target: undefined,

    render_init: function() {
        ProfileCard._render();
    },

    _render: function() {
        var source   = $("#profile_card").html();
        var template = Handlebars.compile(source);
        var compiled = template({"card_name": ProfileCard.name});
        ProfileCard.dom_target.html(compiled);
    }
};
