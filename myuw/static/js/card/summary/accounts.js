var AccountSummaryCard = {
    name: 'AccountSummaryCard',
    dom_target: undefined,
    calls: 0,

    render_init: function(dom_target) {
        AccountSummaryCard.dom_target = dom_target;
        AccountSummaryCard.calls = 0;
        WSData.fetch_library_data(AccountSummaryCard.on_data, AccountSummaryCard.on_data);
        WSData.fetch_hfs_data(AccountSummaryCard.on_data, AccountSummaryCard.on_data);
    },

    on_data: function() {
        AccountSummaryCard.calls++;
        if (AccountSummaryCard.calls < 2) {
            return;
        }
        if (window.term_data.break_year !== window.term_data.year) {
            window.term_data.spans_years = true;
        }

        AccountSummaryCard._render({
            library: WSData.library_data(),
            hfs: WSData.hfs_data(),
            accounts: (WSData.hfs_data() || WSData.library_data()),
            term: window.term_data,
            term_total_weeks: AccountSummaryCard.get_weeks_apart(window.term_data.first_day, window.term_data.last_day),
            term_current_week: AccountSummaryCard.get_weeks_apart(window.term_data.first_day, window.term_data.today_date),
            during_term: (!window.term_data.is_finals && !window.term_data.is_break)
        });
    },

    _render: function(data) {
        var source = $("#account_summary_card").html();
        var template = Handlebars.compile(source);
        AccountSummaryCard.dom_target.html(template(data));
        LogUtils.cardLoaded('AccountSummaryCard', AccountSummaryCard.dom_target);
    },

    get_weeks_apart: function(qs_date, test_date) {
        // qs_date: quarter start date
        var one_day_ms = 24 * 3600 * 1000;
        var one_week_ms = one_day_ms * 7;
        var t1 = qs_date.getTime(); // milliseconds since January 1, 1970
        var qs_day_of_week = qs_date.getDay();
        var qs_prev_sunday = t1 - (one_day_ms * qs_day_of_week);
        var t2 = test_date.getTime();
        if (t2 < qs_prev_sunday) {
            return 0;
        } else {
            return parseInt((t2 - qs_prev_sunday) / one_week_ms) + 1;
        }
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.AccountSummaryCard = AccountSummaryCard;
