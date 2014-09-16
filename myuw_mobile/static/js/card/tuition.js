var TuitionCard = {
    name: 'TuitionCard',
    dom_target: undefined,
    _ajax_count: 0,

    render_init: function() {
        TuitionCard._ajax_count = 2;
        WSData.fetch_tuition_data(TuitionCard.render_upon_data, TuitionCard.render_error);
        WSData.fetch_notice_data(TuitionCard.render_upon_data, TuitionCard.render_error);
        WSData.fetch_course_data_for_term('current', TuitionCard.render_upon_data, CourseCard.render_error);
    },


    render_error: function () {
        $(TuitionCard.dom_target).html(CardWithError.render("Tuition & Fees"));
    },

    render_upon_data: function() {
        if (!TuitionCard._has_all_data()) {
            return;
        }
        TuitionCard._render();
    },

    _render: function () {
        var template_data = WSData.tuition_data(),
            tuition_due_notice,
            display_date,
            due_date;

        //Do not show card if no sections are registered for the current quarter AND balance is 0
        // *AND* there's no due date.  For people who have already paid their tuition.
        // The finanance resource gives a 0.00 balance for everyone.
        if (parseInt(template_data['tuition_accbalance']) === 0
                && WSData.normalized_course_data().sections.length === 0
                && (!template_data["tuition_due"] || !(template_data["tuition_due"].match(/\d+/)))) {
            $(TuitionCard.dom_target).html('');
            return;
        }


        template_data['pce_tuition_dup'] = Notices.get_notices_for_tag("pce_tuition_dup");
        template_data['is_pce'] = false;

        tuition_due_notice = Notices.get_notices_for_tag("tuition_due_date")[0];
        if (tuition_due_notice !== undefined) {
            for (var i = 0; i < tuition_due_notice.attributes.length; i += 1) {
                if (tuition_due_notice.attributes[i].name === "Date") {
                    due_date = new Date(tuition_due_notice.attributes[i].value.replace(/-/g, "/"));
                    display_date = tuition_due_notice.attributes[i].formatted_value
                }
            }
        }
        if (due_date !== undefined) {
            template_data['tuition_date'] = display_date
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
        TuitionCard.dom_target.html(template(template_data));
    },

    _days_from_today: function (date) {
        var today = new Date()
        return Math.ceil((date - today) / (1000*60*60*24));
    },

    _has_all_data: function () {
        if (WSData.tuition_data() && WSData.notice_data() && WSData.normalized_course_data()) {
            return true;
        }
        return false;
    }

};
