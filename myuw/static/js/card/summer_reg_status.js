var SummerRegStatusCard = {
    name: 'SummerRegStatusCard',
    dom_target: undefined,

    render_init: function() {
        if (window.card_display_dates.is_after_start_of_summer_reg_display_period1 || window.card_display_dates.is_after_start_of_summer_reg_display_periodA) {
            WSData.fetch_myplan_data(RegStatusCard.render_upon_data, RegStatusCard.render_error);
            WSData.fetch_notice_data(SummerRegStatusCard.render_upon_data, SummerRegStatusCard.render_error);
            WSData.fetch_oquarter_data(SummerRegStatusCard.render_upon_data, SummerRegStatusCard.render_error);
        }

        if (!window.card_display_dates.is_after_start_of_summer_reg_display_period1) {
            $("#SummerRegStatusCard1").hide();
        }
        if (!window.card_display_dates.is_after_start_of_summer_reg_display_periodA) {
            $("#SummerRegStatusCardA").hide();
        }
    },

    render_upon_data: function() {
        //If more than one data source, multiple callbacks point to this function
        //Delay rendering until all requests are complete
        //Do something smart about not showing error if AJAX is pending
        if (!RegStatusCard._has_all_data()) {
            return;
        }

        SummerRegStatusCard._render();
    },

    render_error: function() {
        $("#SummerRegStatusCardA").html(CardWithError.render("Registration"));
        $("#SummerRegStatusCard1").html(CardWithError.render("Registration"));
    },

    _render: function() {
        var content;
        if (window.card_display_dates.is_after_start_of_summer_reg_display_periodA) {
            content = RegStatusCard._render_for_term('Summer', 'summerA');
            if (!content) {
                $("#SummerRegStatusCardA").hide();
            }
            $("#SummerRegStatusCardA").html(content);
            RegStatusCard._add_events('summerA');
            LogUtils.cardLoaded(SummerRegStatusCard.name, $("#SummerRegStatusCardA"));
        }
        if (window.card_display_dates.is_after_start_of_summer_reg_display_period1) {
            content = RegStatusCard._render_for_term('Summer', 'summer1');

            if (!content) {
                $("#SummerRegStatusCard1").hide();
            }
            $("#SummerRegStatusCard1").html(content);

            RegStatusCard._add_events('summer1');
            LogUtils.cardLoaded(SummerRegStatusCard.name, $("#SummerRegStatusCard1"));
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

