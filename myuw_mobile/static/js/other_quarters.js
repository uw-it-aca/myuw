var Quarters = {
    show_future_quarters: function() {
        showLoading();
        WSData.fetch_oquarter_data(Quarters.render_registered_future_quarters);
    },

    render_registered_future_quarters: function() {
        $('html,body').animate({scrollTop: 0}, 'fast');

        var source = $("#oquarter-header").html();
        var template = Handlebars.compile(source);
        $("#page-header").html(template());

        var data = WSData.oquarter_data();
        source = $("#quarterlist").html();
        template = Handlebars.compile(source);
        $("#courselist").html(template({ terms : data.terms,
                                         not_registered: data.not_registered}));
    }
};
