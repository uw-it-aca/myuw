var PCETuitionCard = {
    render: function (pce_tuition_data) {
        var source = $("#pce_tuition_card").html();
        var template = Handlebars.compile(source);
        return template(pce_tuition_data);
    },

};
