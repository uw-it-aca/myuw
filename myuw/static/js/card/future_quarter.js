var FutureQuarterCard = {
    name: 'FutureQuarterCard',
    dom_target: undefined,

    render_init: function() {
        if (!window.user.student) {
            $("#FutureQuarterCardA").hide();
            $("#FutureQuarterCard1").hide();
            return;
        }

        FutureQuarterCard.dom_target = $("#FutureQuarterCardA");
        WebServiceData.require({oquarter_data: new OQuarterData()},
                               FutureQuarterCard.render);
    },

    render: function (resources) {
        if (FutureQuarterCard.render_error(resources.oquarter_data.error)) {
            return;
        }

        var oquarter_data = resources.oquarter_data.data;

        if (oquarter_data.highlight_future_quarters) {
            $("#FutureQuarterCard1").hide();
        }
        else {
            FutureQuarterCard.dom_target = $('#FutureQuarterCard1');
            $("#FutureQuarterCardA").hide();
        }

        var source = $("#future_quarter_card").html();
        var template = Handlebars.compile(source);

        if (!oquarter_data.terms.length) {
            FutureQuarterCard.dom_target.hide();
        }
        else {
            FutureQuarterCard.dom_target.html(template(oquarter_data));
            LogUtils.cardLoaded(FutureQuarterCard.name, FutureQuarterCard.dom_target);
        }
    },

    render_error: function(oquarter_resource_error) {
        if (oquarter_resource_error) {
            $("#FutureQuarterCard1").hide();
            if (oquarter_resource_error.status === 404) {
                FutureQuarterCard.dom_target.hide();
            } else {
                FutureQuarterCard.dom_target.html(CardWithError.render("Future Quarter Courses"));
            }

            return true;
        }

        return false;
    }

};


// One of these 2 needs to actually call render_init - A for arbitrary.
var FutureQuarterCardA = {
    name: 'FutureQuarterCardA',
    render_init: function() { FutureQuarterCard.render_init(); }
};

var FutureQuarterCard1 = {
    name: 'FutureQuarterCard1',
    render_init: function() {}
};

