var ResourcesCard = {
    name: 'ResourcesCard',
    dom_target: undefined,
    target_group: undefined,

    hide_card: function() {
        return false;
    },

    render_init: function() {
        if (ResourcesCard.hide_card()) {
            $("#ExploreCard").hide();
            return;
        }
        WSData.fetch_resource_data(ResourcesCard.render_upon_data,
                                  ResourcesCard.render_error,
                                   undefined,
                                   true);
    },

    render_upon_data: function () {
        if (WSData.resource_data()) {
            ResourcesCard._render();
        }
    },

    _render: function () {
        Handlebars.registerPartial('resource_content', $("#resource_content").html());
        var data = WSData.resource_data();
        // Hide loading card
        ResourcesCard.dom_target.html("");

        var temp_subcat = data[0].subcategories.Registration;
        $(data).each(function(idx, category){
            var sc = Object.keys(category.subcategories);
            $(sc).each(function(i, subcat){
                var cat_data = category.subcategories[subcat];
                ResourcesCard._append_card(cat_data);
            });
        });

        var name = ResourcesCard.name + ResourcesCard.target_group;
        LogUtils.cardLoaded(name, ResourcesCard.dom_target);
    },

    _append_card: function (subcategory){
        var source = $("#resources_card").html();
        var template = Handlebars.compile(source);
        ResourcesCard.dom_target.append(template(subcategory));
    },


    render_error: function () {
        $("#ExploreCard").hide();
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.ResourcesCard = ResourcesCard;
