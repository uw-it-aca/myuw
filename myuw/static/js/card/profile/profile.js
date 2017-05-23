var ProfileCard = {
    name: 'ProfileCard',
    dom_target: undefined,

    render_init: function() {
        WebServiceData.require({profile_data: new ProfileData()},
                               ProfileCard.render);
    },

    _render: function(resources) {
        var profile_resource = resources.profile_data;
        var profile_data = profile_resource.data;
        var source   = $("#profile_card").html();
        var template = Handlebars.compile(source);
        profile_data.card_name = ProfileCard.name;
        var compiled = template(profile_data);
        ProfileCard.dom_target.html(compiled);
    }
};
