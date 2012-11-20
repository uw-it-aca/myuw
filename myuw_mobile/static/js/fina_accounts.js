var FinaAccounts = {
    show_balances: function() {
        showLoading();
        WSData.fetch_financial_data(FinaAccounts.render_balances);
    },

    render_balances: function() {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var balances = WSData.financial_data();

        var source   = $("#finabala-header").html();
        var template = Handlebars.compile(source);
        $("#page-header").html(template(
                {time: balances.asof_time, 
                 date: balances.asof_date}));

         source   = $("#financial_balances").html();
         template = Handlebars.compile(source);
         var amount_css = "amount"
         if ( balances.husky_card < 1.00 ) {
            amount_css = "amount-low" 
            }
         $("#courselist").html(template(
                {color: amount_css,
                 husky_card_balance: balances.husky_card,
                 residence_hall_dining_balance: balances.residence_hall_dining }));
         }
};
