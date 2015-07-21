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
        }
        else {
            MyGradCard.dom_target.html(template(mygrad_data));
        }
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
