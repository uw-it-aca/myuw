var ThriveCard = {
    name: 'ThriveCard',
    dom_target: undefined,

    render_init: function() {
        if (window.user.fyp) {
            WebServiceData.require({thrive_data: new ThriveData()}, ThriveCard.render);
            return;
        }
        $("#ThriveCard").hide();
    },

    render: function (resources) {
        var thrive_resource = resources.thrive_data;
        if (ThriveCard.render_error(thrive_resource.error)) {
            return;
        }

        Handlebars.registerPartial('thrive_highlight', $("#thrive_highlight").html());
        Handlebars.registerPartial('thrive_learnmore', $("#thrive_learnmore").html());
        var thrive = thrive_resource.data;
        var source = $("#thrive_card").html();
        var template = Handlebars.compile(source);
        ThriveCard.dom_target.html(template(thrive));
        LogUtils.cardLoaded(ThriveCard.name, ThriveCard.dom_target);
    },

    render_error: function (thrive_resource_error) {
        if (thrive_resource_error) {
            $("#ThriveCard").hide();
            return true;
        }

        return false;
    }
};
