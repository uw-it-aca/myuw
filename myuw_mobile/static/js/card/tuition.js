var TuitionCard = {
    render: function (tuition_data) {
        var template_data = tuition_data,
        tuition_due_notice, display_date,
            due_date;
        template_data['pce_tuition_dup'] = Notices.get_notices_for_tag("pce_tuition_dup");

        tuition_due_notice = Notices.get_notices_for_tag("tuition_balance")[0];
        for (var i = 0; i < tuition_due_notice.attributes.length; i += 1){
            if (tuition_due_notice.attributes[i].name === "Date"){
                due_date = new Date(tuition_due_notice.attributes[i].value.replace(/-/g, "/"));
                display_date = tuition_due_notice.attributes[i].formatted_value
            }
        }
        if (due_date !== undefined) {
            template_data['tuition_date'] = display_date
            template_data['tuition_date_offset'] = TuitionCard._days_from_today(due_date);
        }

        var source = $("#tuition_card").html();
        var template = Handlebars.compile(source);
        return template(tuition_data);
    },

    _days_from_today: function (date) {
        var today = new Date()
        return Math.ceil((date - today) / (1000*60*60*24));
    }

};
