var GradCommitteeCard = {
    name: 'GradCommitteeCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_mygrad_data(GradCommitteeCard.render_upon_data, GradCommitteeCard.show_error);
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

        for (var k = 0; k < mygrad_data.committees.length; k += 1) {
            var members = mygrad_data.committees[k].members;
            for (var j = 0; j < members.length; j += 1) {
                if (members[j].member_type === "member") {
                    members[j].member_type = null;
                }
            }
        }
        GradCommitteeCard.dom_target.html(template(mygrad_data));
    },

    _has_all_data: function () {
        if (WSData.mygrad_data()) {
            return true;
        }
        return false;
    },

    show_error: function() {
        GradCommitteeCard.dom_target.html(CardWithError.render("GradCommittee"));
    }

};
