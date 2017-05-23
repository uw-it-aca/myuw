var TuitionCard = {
    name: 'TuitionCard',
    dom_target: undefined,

    render_init: function() {
        TuitionCard.dom_target =$('#TuitionCard');
        if (!window.user.student) {
            TuitionCard.dom_target.hide();
            return;
        }

        WebServiceData.require({notice_data: new NoticeData(),
                                tuition_data: new TuitionData()},
                               TuitionCard.render);
    },

    render_error: function (notice_resource_error, tuition_resource_error) {
        if (notice_resource_error || tuition_resource_error) {
            // notice never returns 404.
            if (notice_resource_error && notice_resource_error.status === 404 ||
                tuition_resource_error && tuition_resource_error.status === 404) {
                // not student or SDB can't find the regid
                TuitionCard.dom_target.hide();
            } else {
                var raw = CardWithError.render("Tuition & Fees");
                TuitionCard.dom_target.html(raw);
            }
            return true;
        }

        return false;
    },

    process_tuition: function(data) {
        var is_credit = false;
        if (data.match(" CR")) {
            is_credit = true;
            data = data.replace(" CR", "");
        }
        return {
            tuition: data,
            is_credit: is_credit
        };
    },

    render: function (resources) {
        var notice_resource = resources.notice_data;
        var tuition_resource = resources.tuition_data;
        if (TuitionCard.render_error(notice_resource.error, tuition_resource.error)) {
            return;
        }

        // _render should be called only once.
        if (renderedCardOnce(TuitionCard.name)) {
            return;
        }

        var template_data = tuition_resource.data,
            tuition_due_notice,
            display_date,
            due_date,
            has_credit_values;

        template_data.pce_tuition_dup = Notices.get_notices_for_tag("pce_tuition_dup");
        template_data.is_pce = false;

        if (template_data.pce_accbalance == '0.00') {
            template_data.pce_accbalance = 0;
        }

        has_credit_values = TuitionCard.process_tuition(template_data.tuition_accbalance);
        template_data.plain_tuition = has_credit_values.tuition;
        template_data.is_credit = has_credit_values.is_credit;

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

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.TuitionCard = TuitionCard;
