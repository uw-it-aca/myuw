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
         var hc_amount_css = "amount"
         if ( balances.husky_card < 1.00 ) {
            hc_amount_css = "amount-low" 
            }
         var hc_negative = ""
         if ( balances.husky_card < 0.00 ) {
            hc_negative = "<span class=amount-low>-</span>"
            }

         var din_amount_css = "amount"
         if ( balances.residence_hall_dining < 1.00 ) {
            din_amount_css = "amount-low" 
            }
         var din_negative = ""
         if ( balances.residence_hall_dining < 0.00 ) {
            din_negative = "<span class=amount-low>-</span>"
            }
         $("#courselist").html(template(
                {hc_negative: hc_negative,
                 hc_color: hc_amount_css,
                 husky_card_balance: Math.abs(balances.husky_card),
                 din_negative: din_negative,
                 din_color: din_amount_css,
                 residence_hall_dining_balance: Math.abs(balances.residence_hall_dining) }));
         }
};
