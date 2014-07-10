var PCETuitionCard = {
    name: 'PCETuitionCard',
    dom_target: undefined,
    _ajax_count: 0,

    render_init: function() {
        PCETuitionCard._ajax_count = 2;
        WSData.fetch_tuition_data(PCETuitionCard.render_upon_data);
        WSData.fetch_notice_data(PCETuitionCard.render_upon_data);
    },

    render_upon_data: function() {
        PCETuitionCard._ajax_count -= 1;
        if(!PCETuitionCard._has_all_data()  && PCETuitionCard._ajax_count === 0){
            PCETuitionCard.dom_target.html(CardWithError.render());
            return;
        }
        PCETuitionCard._render();
    },

    _render: function () {
        var template_data = WSData.tuition_data(),
            tuition_due_notice,
            display_date,
            due_date;
        template_data['pce_tuition_dup'] = Notices.get_notices_for_tag("pce_tuition_dup");
        template_data['is_pce'] = true;
        template_data['tuition_accbalance'] = template_data['pce_tuition_accbalance'];

        tuition_due_notice = Notices.get_notices_for_tag("tuition_balance")[0];
        for (var i = 0; i < tuition_due_notice.attributes.length; i += 1){
            if (tuition_due_notice.attributes[i].name === "Date"){
                due_date = new Date(tuition_due_notice.attributes[i].value.replace(/-/g, "/"));
                display_date = tuition_due_notice.attributes[i].formatted_value
            }
        }
        if (due_date !== undefined) {
            template_data['tuition_date'] = display_date;
            template_data['tuition_date_offset'] = TuitionCard._days_from_today(due_date);

            //Alert banners
            if(parseFloat(template_data['tuition_accbalance']) > 0){
                if(template_data['tuition_date_offset'] === 0){
                    template_data['due_today'] = true;
                }
                if (template_data['tuition_date_offset'] < 0){
                    template_data['past_due'] = true;
                }
            }
        }
        template_data['has_balance'] = parseInt(template_data['tuition_accbalance']) > 0;

        var source = $("#tuition_card").html();
        var template = Handlebars.compile(source);
        PCETuitionCard.dom_target.html(template(template_data));
    },

    _days_from_today: function (date) {
        var today = new Date()
        return Math.ceil((date - today) / (1000*60*60*24));
    },

    _has_all_data: function () {
        if (WSData.tuition_data() && WSData.notice_data()) {
            return true;
        }
        return false;
    }

};
