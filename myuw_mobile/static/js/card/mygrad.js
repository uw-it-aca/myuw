var MyGradCard = {
    name: 'MyGradCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_mygrad_data(MyGradCard.render_upon_data, MyGradCard.show_error);
    },

    render_upon_data: function() {
        if (!MyGradCard._has_all_data()) {
            return;
        }
        MyGradCard._render(WSData.mygrad_data());
    },

    _render: function (mygrad_data) {
        var source = $("#mygrad_card_content").html();
        var template = Handlebars.compile(source);
        if (!mygrad_data.degrees && !mygrad_data.committees && !mygrad_data.leaves && !mygrad_data.petitions) {
            MyGradCard.dom_target.hide();
            return;
        }

        for (var i = 0; i < mygrad_data.committees.length; i += 1) {
            var members = mygrad_data.committees[i].members;
            for (var j = 0; j < members.length; j += 1) {
                if (members[j].member_type === "member") {
                    members[j].member_type = null;
                }
            }
        }
        MyGradCard.dom_target.html(template(mygrad_data));
    },

    _has_all_data: function () {
        if (WSData.mygrad_data()) {
            return true;
        }
        return false;
    },

    show_error: function() {
        MyGradCard.dom_target.html(CardWithError.render("MyGrad"));
    }

};
