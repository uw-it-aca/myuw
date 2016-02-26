var GradCommitteeCard = {
    name: 'GradCommitteeCard',
    dom_target: undefined,

    render_init: function() {
        if (!window.user.grad) {
            $("#GradCommitteeCard").hide();
            return;
        }

        WSData.fetch_mygrad_data(GradCommitteeCard.render_upon_data, GradCommitteeCard.render_error);
    },

    render_upon_data: function() {
        if (!GradCommitteeCard._has_all_data()) {
            return;
        }
        GradCommitteeCard._render(WSData.mygrad_data());
    },

    _render: function (mygrad_data) {
        var source = $("#gradcommittee_card_content").html();
        var template = Handlebars.compile(source);
        if (!mygrad_data.committees) {
            GradCommitteeCard.dom_target.hide();
            return;
        }
        if (mygrad_data.comm_err) {
            GradCommitteeCard.render_error();
            return;
        }

        GradCommitteeCard.dom_target.html(template(mygrad_data));
    },

    _has_all_data: function () {
        if (WSData.mygrad_data()) {
            return true;
        }
        return false;
    },

    render_error: function(status) {
        var raw = CardWithError.render("Your Committees");
        GradCommitteeCard.dom_target.html(raw);
    }

};
