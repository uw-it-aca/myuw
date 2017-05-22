var ProfileCard = {
    name: 'ProfileCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_profile_data(ProfileCard._render);
    },

    _render: function() {
        var profile_data = WSData.profile_data();
        var source   = $("#profile_card").html();
        var template = Handlebars.compile(source);
        profile_data.card_name = ProfileCard.name;
        var compiled = template(profile_data);
        ProfileCard.dom_target.html(compiled);
    }
};
