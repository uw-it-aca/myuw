var SummerRegStatusCard = {
    name: 'SummerRegStatusCard',
    dom_target: undefined,
    label: undefined,

    render_init: function() {
        if (window.user.student && window.card_display_dates.is_after_start_of_summer_reg_display_periodA) {
            $("#SummerRegStatusCard1").hide();
            SummerRegStatusCard.label = 'summerA';
            SummerRegStatusCard.name = 'SummerRegStatusCardA';
            SummerRegStatusCard.dom_target = $('#SummerRegStatusCardA');
        } else if (window.user.student && window.card_display_dates.is_after_start_of_summer_reg_display_period1) {
            $("#SummerRegStatusCardA").hide();
            SummerRegStatusCard.label = 'summer1';
            SummerRegStatusCard.name = 'SummerRegStatusCard1';
            SummerRegStatusCard.dom_target = $('#SummerRegStatusCard1');
        } else {
            $("#SummerRegStatusCardA").hide();
            $("#SummerRegStatusCard1").hide();
            return;
        }

        WSData.fetch_notice_data(SummerRegStatusCard.render_upon_data,
                                 SummerRegStatusCard.render_error);
        WSData.fetch_oquarter_data(SummerRegStatusCard.render_upon_data,
                                   SummerRegStatusCard.render_error);
    },

    render_upon_data: function() {
        if (!RegStatusCard._has_all_data()) {
            return;
        }

        var year = WSData.oquarter_data().next_term_data.year;
        if (! window.card_display_dates.myplan_peak_load &&
            ! WSData.myplan_data(year, "Summer")) {
            WSData.fetch_myplan_data(year, "Summer",
                                     SummerRegStatusCard.render_upon_data,
                                     SummerRegStatusCard.render_error);
            return;
        }

        // _render should be called only once.
        // if (renderedCardOnce(SummerRegStatusCard.name)) {
        //    return;
        // }
        SummerRegStatusCard._render();
    },

    render_error: function(status) {
        // none of the api data returns 404.
        // any data failure, display error
        SummerRegStatusCard.dom_target.html(CardWithError.render("Summer Registration"));
    },

    _render: function() {
        var year = WSData.oquarter_data().next_term_data.year;
        var myplan_data;
        if (! window.card_display_dates.myplan_peak_load) {
            myplan_data = WSData.myplan_data(year, "Summer");
        }

        if (window.card_display_dates.myplan_peak_load || myplan_data) {
            var content = RegStatusCard._render_for_term(myplan_data,
                                                         'Summer',
                                                         SummerRegStatusCard.label);
            if (!content) {
                SummerRegStatusCard.dom_target.hide();
                return;
            }
            SummerRegStatusCard.dom_target.html(content);
            RegStatusCard._add_events(SummerRegStatusCard.label);
            LogUtils.cardLoaded(SummerRegStatusCard.name,
                                SummerRegStatusCard.dom_target);
        }
    }
};

// One of these 2 needs to actually call render_init - A for arbitrary.
var SummerRegStatusCardA = {
    name: 'SummerRegStatusCardA',
    render_init: function() { SummerRegStatusCard.render_init(); }
};

var SummerRegStatusCard1 = {
    name: 'SummerRegStatusCard1',
    render_init: function() {}
};
