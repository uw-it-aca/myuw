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

        if (mygrad_data.committees !== null) {
            for (var k = 0; k < mygrad_data.committees.length; k += 1) {
                var members = mygrad_data.committees[k].members;
                for (var j = 0; j < members.length; j += 1) {
                    if (members[j].member_type === "member") {
                        members[j].member_type = null;
                    }
                }
            }
        }
        MyGradCard.dom_target.html(template(mygrad_data));
        MyGradCard.add_events();
    },

    _has_all_data: function () {
        if (WSData.mygrad_data()) {
            return true;
        }
        return false;
    },

    add_events: function() {
        $("#toggle_grad_committees").on("click", function(ev) {
            ev.preventDefault();
            $("#grad_committee_reqs").toggleClass("slide-show");
            var card = "MyGradCard";

            if ($("#grad_committee_reqs").hasClass("slide-show")) {
                $("#toggle_grad_committees").text("HIDE COMMITTEES");
                $("#toggle_grad_committees").attr("title", "Hide Committees");
                $("#grad_committee_reqs").attr("aria-hidden", "false");
                window.myuw_log.log_card(card, "expand committees");
            }
            else {
                $("#toggle_grad_committees").text("SHOW COMMITTEES");
                $("#toggle_grad_committees").attr("title", "Expand to show Committees");
                $("#grad_committee_reqs").attr("aria-hidden", "true");
                window.myuw_log.log_card(card, "collapse committees");

                setTimeout(function() {
                    $("#toggle_grad_committees").text("SHOW COMMITTEES");
                }, 700);
            }
        });
    },

    show_error: function() {
        MyGradCard.dom_target.html(CardWithError.render("MyGrad"));
    }

};
