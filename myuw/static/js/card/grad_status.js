var GradStatusCard = {
    name: 'GradStatusCard',
    dom_target: undefined,

    render_init: function() {
        if (!window.user.grad) {
            $("#GradStatusCard").hide();
            return;
        }

        WebServiceData.require({mygrad_data: new MyGradData()}, GradStatusCard.render);
    },

    render: function (resources) {
        var mygrad_resource = resources.mygrad_data;

        if (GradStatusCard.render_error(mygrad_resource.error)) {
            return;
        }

        var mygrad_data = mygrad_resource.data;
        var source = $("#gradstatus_card_content").html();
        var template = Handlebars.compile(source);
        if (!mygrad_data.degrees && !mygrad_data.leaves && !mygrad_data.petitions) {
            GradStatusCard.dom_target.hide();
            return;
        }

        if (mygrad_data.degree_err && mygrad_data.leave_err && mygrad_data.petit_err) {
            GradStatusCard.render_error(true);
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

    render_error: function(mygrad_resource_error) {
        if (mygrad_resource_error) {
            var raw = CardWithError.render("Graduate Request Status");
            GradStatusCard.dom_target.html(raw);
            return true;
        }

        return false;
    }
};
