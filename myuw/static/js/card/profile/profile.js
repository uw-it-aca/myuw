var CommonProfileCard = {
    name: 'CommonProfileCard',
    dom_target: undefined,

    render_init: function() {
        WebServiceData.require({directory_data: new DirectoryData()},
                               CommonProfileCard.render);
    },

    render: function(resources) {
        var directory_resource = resources.directory_data;
        var directory_data = directory_resource.data
        var source   = $("#common_profile_card").html();
        var template = Handlebars.compile(source);
        directory_data.card_name = CommonProfileCard.name;
        var compiled = template({
            display_name: directory_data.display_name,
            full_name: directory_data.full_name,
            has_preferred: (directory_data.display_name !== directory_data.full_name)
        });
        CommonProfileCard.dom_target.html(compiled);
    }
};
