var PCETuitionCard = {
    render: function (fina_notices) {
        var source = $("#pce_tuition_card").html();

        var template = Handlebars.compile(source);
        return template();
    },

};
