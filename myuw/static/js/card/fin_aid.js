var FinAidCard = {
    fina_notices: null,

    render_init: function (fina_notices) {
        FinAidCard.fina_notices = fina_notices;
        WebServiceData.require({tuition_data: new TuitionData()}, FinAidCard.render);
    },

    render: function (resources) {
        var tuition_data = resources.tuition_data.data;
        var source = $("#fin_aid_card").html();
        var template = Handlebars.compile(source);
        return template({"balances": tuition_data,
                         "fina_notices": fina_notices.notices});
    },
};
