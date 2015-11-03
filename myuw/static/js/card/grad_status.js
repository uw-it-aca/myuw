var GradStatusCard = {
    name: 'GradStatusCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_mygrad_data(GradStatusCard.render_upon_data, GradStatusCard.show_error);
    },

    render_upon_data: function() {
        if (!GradStatusCard._has_all_data()) {
            return;
        }
        GradStatusCard._render(WSData.mygrad_data());
    },

    _render: function (mygrad_data) {
        var source = $("#gradstatus_card_content").html();
        var template = Handlebars.compile(source);
        if (!mygrad_data.degrees && !mygrad_data.leaves && !mygrad_data.petitions) {
            GradStatusCard.dom_target.hide();
            return;
        }

        if (mygrad_data.petitions !== null) {
            for (var i = 0; i < mygrad_data.petitions.length; i += 1) {
                if (mygrad_data.petitions[i].dept_recommend === "Pending" || mygrad_data.petitions[i].dept_recommend === "Withdraw") {
                    mygrad_data.petitions[i].gradschool_decision = null;
                }
                if (mygrad_data.petitions[i].gradschool_decision === "Approved") {
                    mygrad_data.petitions[i].dept_recommend = null;
                }
            }
        }
        GradStatusCard.dom_target.html(template(mygrad_data));
    },

    _has_all_data: function () {
        if (WSData.mygrad_data()) {
            return true;
        }
        return false;
    },

    show_error: function() {
        GradStatusCard.dom_target.html(CardWithError.render("GradStatus"));
    }

};
