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

        var sorted_subcategories = {};

        $(data).each(function(idx, category){
            var sc = Object.keys(category.subcategories);
            $(sc).each(function(i, subcat){
                var cat_data = category.subcategories[subcat];
                sorted_subcategories[cat_data.order] = cat_data;
            });
        });
        for(var i=0; i < Object.keys(sorted_subcategories).length; i++){
            ResourcesCard._append_card(sorted_subcategories[i]);
        }

        var name = ResourcesCard.name + ResourcesCard.target_group;
        ResourcesCard.init_events();
        LogUtils.cardLoaded(name, ResourcesCard.dom_target);
    },

    init_events: function () {
        $(".category-pin, .category-unpin").click(function(ev){
            var cat_id = $(ev.target).val(),
                pin = true;
            if ($(ev.target).attr('class').indexOf('unpin') > -1){
                pin = false;
                $(ev.target).addClass('hidden');
                $(ev.target).siblings('.category-pin').removeClass('hidden');
                $(ev.target).closest(".resources-card").hide();
            } else {
                $(ev.target).addClass('hidden');
                $(ev.target).siblings('.category-unpin').removeClass('hidden');
            }

            Resources.handle_pin_click(cat_id, pin);
        });
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
