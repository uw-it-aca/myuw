var TuitionCard = {
    name: 'TuitionCard',
    dom_target: undefined,
    _ajax_count: 0,

    render_init: function() {
        if (!window.user.student) {
            $("#TuitionCard").hide();
            return;
        }
        TuitionCard._ajax_count = 2;
        WSData.fetch_tuition_data(TuitionCard.render_upon_data, TuitionCard.render_error);
        WSData.fetch_notice_data(TuitionCard.render_upon_data, TuitionCard.render_error);
    },

    _has_all_data: function () {
        if (WSData.tuition_data() && WSData.notice_data()) {
            return true;
        }
        return false;
    },

    render_error: function (status) {
        if (status === 404) {
            TuitionCard.dom_target.hide();
            return;
        }
        var raw = CardWithError.render("Tuition & Fees");
        TuitionCard.dom_target.html(raw);
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

        template_data.pce_tuition_dup = Notices.get_notices_for_tag("pce_tuition_dup");
        template_data.is_pce = false;

        tuition_due_notice = Notices.get_notices_for_tag("tuition_due_date")[0];
        if (tuition_due_notice !== undefined) {
            for (var i = 0; i < tuition_due_notice.attributes.length; i += 1) {
                if (tuition_due_notice.attributes[i].name === "Date") {
                    due_date = new Date(tuition_due_notice.attributes[i].value.replace(/-/g, "/"));
                    display_date = tuition_due_notice.attributes[i].formatted_value;
                }
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
        var finaid_tags = ["tuition_aidhold_title",
                           "tuition_missingdocs_title",
                           "tuition_loanpromissory_title",
                           "tuition_loancounseling_title",
                           "tuition_acceptreject_title",
                           "tuition_disbursedateA_title",
                           "tuition_disbursedateB_title",
                           "tuition_direct_deposit_title",
                           "tuition_aid_prioritydate_title",
                           "tuition_aid_reminder_title",
                           "tuition_summeraid_date_title",
                           "tuition_summeraid_avail_title"
                          ];
        template_data.finaid_notices = Notices.get_ordered_finaid_notices(finaid_tags);
        var source = $("#tuition_card").html();
        var template = Handlebars.compile(source);
        TuitionCard.dom_target.html(template(template_data));
        LogUtils.cardLoaded(TuitionCard.name, TuitionCard.dom_target);
        TuitionCard._init_events();
    },

    _days_from_today: function (date) {
        var today = new Date();
        return Math.ceil((date - today) / (1000*60*60*24));
    },

    _init_events: function(){
        $(".finaid-panel-default").find('a').each(function(idx, elm){
            $(elm).on('click', function(e){
                var content = $(e.target).parents('li').find('.finaid-panel-collapse');
                if(content.attr('aria-hidden')){
                    content.attr('aria-hidden', false);
                } else{
                    content.attr('aria-hidden', true);
                }
            });
        });
    }
};
