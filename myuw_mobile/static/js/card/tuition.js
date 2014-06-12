var TuitionCard = {
    render: function (tuition_data) {
        var template_data = tuition_data;
        template_data['pce_tuition_dup'] = Notices.get_notices_for_tag("pce_tuition_dup");
        var source = $("#tuition_card").html();
        var template = Handlebars.compile(source);
        return template(tuition_data);
    },

};
