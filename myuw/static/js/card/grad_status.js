var GradStatusCard = {
    name: 'GradStatusCard',
    dom_target: undefined,

    render_init: function() {
        if (!window.user.grad) {
            $("#GradStatusCard").hide();
            return;
        }

        WSData.fetch_mygrad_data(GradStatusCard.render_upon_data, GradStatusCard.render_error);
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
        if (mygrad_data.degree_err && mygrad_data.leave_err && mygrad_data.petit_err) {
            GradStatusCard.render_error();
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

    render_error: function(status) {
        var raw = CardWithError.render("Graduate Request Status");
        GradStatusCard.dom_target.html(raw);
    }

};
