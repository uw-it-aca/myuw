var AccountSummaryCard = {
    name: 'AccountSummaryCard',
    dom_target: undefined,
    calls: 0,

    render_init: function(dom_target) {
        AccountSummaryCard.dom_target = dom_target;
        AccountSummaryCard.calls = 0;
        WSData.fetch_library_data(AccountSummaryCard.on_data, AccountSummaryCard.on_data);
        WSData.fetch_hfs_data(AccountSummaryCard.on_data, AccountSummaryCard.on_data);
//        WSData.fetch_library_data(AccountSummaryCard.on_data, AccountSummaryCard.on_error);
    },

    on_data: function() {
        AccountSummaryCard.calls++;
        if (AccountSummaryCard.calls < 2) {
            return;
        }
        AccountSummaryCard._render({
            library: WSData.library_data(),
            hfs: WSData.hfs_data(),
            term: window.term_data,
            term_total_weeks: AccountSummaryCard.get_weeks_apart(window.term_data.first_day, window.term_data.last_day),
            term_current_week: AccountSummaryCard.get_weeks_apart(window.term_data.first_day, window.term_data.today_date),
        });
    },

    _render: function(data) {
        var source = $("#account_summary_card").html();
        var template = Handlebars.compile(source);
        AccountSummaryCard.dom_target.html(template(data));
    },

    get_weeks_apart: function(date1, date2) {
        var total_weeks = 0;
        var test_date;
        if (date2 < date1) {
            return total_weeks;
        }
        if (AccountSummaryCard._dates_equal(date1, date2)) {
            return 1;
        }

        test_date = new Date(date1.getFullYear(), date1.getMonth(), date1.getDate());
        var original_monday_week = true;
        if (test_date.getDay() != 1) {
            original_monday_week = false;
            total_weeks++;
            test_date.setDate(test_date.getDate() + 7 - test_date.getDay());

            if (test_date > date2) {
                return total_weeks;
            }
        }

        while (true) {
            if (original_monday_week) {
                if (AccountSummaryCard._dates_equal(test_date, date2)) {
                    return total_weeks+1;
                }
            }
            if (test_date >= date2) {
                return total_weeks;
            }
            test_date.setDate(test_date.getDate() + 7);
            total_weeks++;
        }
    },

    _dates_equal: function(date1, date2) {
        return !(date1 > date2 || date1 < date2);
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.AccountSummaryCard = AccountSummaryCard;
