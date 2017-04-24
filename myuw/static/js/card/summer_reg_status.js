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
        WebServiceData.require({notice_data: new NoticeData(),
                                oquarter_data: new OQuarterData()},
                               SummerRegStatusCard.pre_render);
    },

    render_error: function(notice_resource_error, oquarter_resource_error) {
        if (notice_resource_error || oquarter_resource_error) {
            // none of the api data returns 404.
            // any data failure, display error
            SummerRegStatusCard.dom_target.html(CardWithError.render("Summer Registration"));
            return true;
        }

        return false;
    },

    pre_render: function(resources) {
        // _render should be called only once.
        if (renderedCardOnce(SummerRegStatusCard.name)) {
            return;
        }

        var notice_resource = resources.notice_data;
        var oquarter_resource = resources.oquarter_data;
        if (SummerRegStatusCard.render_error(notice_resource.error,
                                             oquarter_resource.error)) {
            return;
        }

        var oquarter_data = oquarter_resource.data;
        var year = oquarter_data.next_term_data.year;
        if (! window.card_display_dates.myplan_peak_load) {
            WebServiceData.require({myplan_data: new MyPlanData(year, "Summer")},
                                   SummerRegStatusCard.render,
                                   [oquarter_resource]);
            return;
        }

        SummerRegStatusCard.render(resources);
    },

    render: function(oquarter_resource, myplan_resources) {
        var oquarter_data = oquarter_resource.data;

        var year = oquarter_data.next_term_data.year;
        var myplan_data;
        if (! window.card_display_dates.myplan_peak_load) {
            if (myplan_resources) {
                myplan_data = myplan_resources.myplan_data.data;
            }
        }

        if (window.card_display_dates.myplan_peak_load || myplan_data) {
            var content = RegStatusCard._render_for_term(myplan_data,
                                                         'Summer',
                                                         oquarter_data,
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
