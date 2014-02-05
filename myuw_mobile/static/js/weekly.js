var Weekly = {
    show_current_week: function() {
        showLoading();
        WSData.fetch_current_week_data(Weekly.render_week);
    },

    render_week: function(data) {

        var current_week = data["current_week"];
        var template;

        if (current_week > 0 && current_week < 11) {
            var name = "#week"+current_week+"_outline";

            if ($(name).length) {
                var source = $(name).html();
                template = Handlebars.compile(source);
            }
        }

        if (!template) {
            var source = $("#week_other_outline").html();
            template = Handlebars.compile(source);
        }

        $("#courselist").html(template());
    }
};
