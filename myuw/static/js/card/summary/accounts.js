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
            term: window.term_data
        });
    },

    _render: function(data) {
        var source = $("#account_summary_card").html();
        var template = Handlebars.compile(source);
        AccountSummaryCard.dom_target.html(template(data));
    }
};
