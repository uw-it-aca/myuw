var PCETuitionCard = {
    name: 'PCETuitionCard',
    dom_target: undefined,

    render_init: function() {
        WebServiceData.require({notice_data: new NoticeData(),
                                tuition_data: new TuitionData()},
                               PCETuitionCard.render);
    },

    render_error: function (notice_resource_error, tuition_resource_error) {
        if (notice_resource_error, tuition_resource_error) {
            PCETuitionCard.dom_target.html(CardWithError.render("PCE Tuition Card"));
            return true;
        }

        return false;
    },

    render: function (resources) {
        // _render should be called only once.
        if (renderedCardOnce(PCETuitionCard.name)) {
            return;
        }

        var notice_resource = resources.notice_data;
        var tuition_resource = resources.tuition_data;
        if (PCETuitionCard.render_error(notice_resource.error, tuition_resource.error)) {
            return;
        }

        var template_data = tuition_resource.data,
            tuition_due_notice,
            display_date,
            due_date;
        template_data.pce_tuition_dup = Notices.get_notices_for_tag("pce_tuition_dup");
        template_data.is_pce = true;
        template_data.tuition_accbalance = template_data.pce_tuition_accbalance;

        tuition_due_notice = Notices.get_notices_for_tag("tuition_balance")[0];
        for (var i = 0; i < tuition_due_notice.attributes.length; i += 1){
            if (tuition_due_notice.attributes[i].name === "Date"){
                due_date = new Date(tuition_due_notice.attributes[i].value.replace(/-/g, "/"));
                display_date = tuition_due_notice.attributes[i].formatted_value;
            }
        }
        if (due_date !== undefined) {
            template_data.tuition_date = display_date;
            template_data.tuition_date_offset = TuitionCard._days_from_today(due_date);

            //Alert banners
            if(parseFloat(template_data.tuition_accbalance) > 0){
                if(template_data.tuition_date_offset === 0){
                    template_data.due_today = true;
                }
                if (template_data.tuition_date_offset < 0){
                    template_data.past_due = true;
                }
            }
        }
        template_data.has_balance = parseInt(template_data.tuition_accbalance) > 0;

        var source = $("#tuition_card").html();
        var template = Handlebars.compile(source);
        PCETuitionCard.dom_target.html(template(template_data));
        LogUtils.cardLoaded(PCETuitionCard.name, PCETuitionCard.dom_target);
    },

    _days_from_today: function (date) {
        var today = new Date();
        return Math.ceil((date - today) / (1000*60*60*24));
    }

};
