var GradCommitteeCard = {
    name: 'GradCommitteeCard',
    dom_target: undefined,

    render_init: function() {
        if (!window.user.grad) {
            $("#GradCommitteeCard").hide();
            return;
        }

        WebServiceData.require({mygrad_data: new MyGradData()}, GradCommitteeCard.render);
    },

    render: function (resources) {
        var mygrad_resource = resources.mygrad_data;

        if (GradCommitteeCard.render_error(mygrad_resource.error)) {
            return;
        }

        var mygrad_data = mygrad_resource.data;
        var source = $("#gradcommittee_card_content").html();
        var template = Handlebars.compile(source);
        if (!mygrad_data.committees) {
            GradCommitteeCard.dom_target.hide();
            return;
        }
        if (mygrad_data.comm_err) {
            GradCommitteeCard.render_error(true);
            return;
        }

        GradCommitteeCard.dom_target.html(template(mygrad_data));
    },

    render_error: function(mygrad_resource_error) {
        if (mygrad_resource_error) {
            var raw = CardWithError.render("Your Committees");
            GradCommitteeCard.dom_target.html(raw);
            return true;
        }

        return false;
    }

};
