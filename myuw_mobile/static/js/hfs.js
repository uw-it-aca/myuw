var HfsAccounts = {
    show_balances: function() {
        showLoading();
        WSData.fetch_hfs_data(HfsAccounts.render_balances);
    },

    render_balances: function() {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var balances = WSData.hfs_data();

        var source   = $("#hfs-header").html();
        var template = Handlebars.compile(source);
        $("#page-header").html(template(
                {time: balances.asof_time, 
                 date: balances.asof_date}));

         source   = $("#hfs_balances").html();
         template = Handlebars.compile(source);
         var hc_amount_css = "amount"
         if ( balances.husky_card < 1.00 ) {
            hc_amount_css = "amount-low" 
            }
         var hc_negative = ""
         if ( balances.husky_card < 0.00 ) {
            hc_negative = "-"
            }

         var din_amount_css = "amount"
         if ( balances.residence_hall_dining < 1.00 ) {
            din_amount_css = "amount-low" 
            }
         var din_negative = ""
         if ( balances.residence_hall_dining < 0.00 ) {
            din_negative = "-"
            }
         $("#main-content").html(template({
            hc_color: hc_amount_css,
            hc_negative: hc_negative,
            husky_card_balance: Math.abs(balances.husky_card),
            din_color: din_amount_css,
            din_negative: din_negative,
            residence_hall_dining_balance: Math.abs(balances.residence_hall_dining) }));
         }
};
