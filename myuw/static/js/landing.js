var Landing = {
    is_desktop: undefined,

    render: function() {
        showLoading();
        Landing.make_html();
    },

    make_html: function () {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var landing_source = $("#landing").html();
        var template = Handlebars.compile(landing_source);

        $("#main-content").html(template());

        NoticeBanner.render_init($("#notice_banner_location"));

        AccountSummaryCard.render_init($("#landing_summaries"));

        Landing.load_cards_for_viewport();
        // Set initial display state
        Landing.is_desktop = get_is_desktop();

        // Monitor for viewport changes and reorder cards if needed
        $(window).resize(function(){
            if (Landing.is_desktop !== get_is_desktop()){
                Landing.load_cards_for_viewport();
                Landing.is_desktop = get_is_desktop();
            }
        });
    },

    load_cards_for_viewport: function() {
        if (get_is_desktop()) {
            Landing._load_desktop_cards();
        } else {
            Landing._load_mobile_cards();
        }
    },

    _load_desktop_cards: function() {
        Landing._reset_content_divs();

        Cards.load_cards_in_order(Landing._get_desktop_body_cards(),
                                  $("#landing_content_cards"));
        Cards.load_cards_in_order(Landing._get_desktop_sidebar_cards(),
                                  $("#landing_accounts_cards"));
    },

    _get_desktop_body_cards: function() {
        var desktop_body_cards = [];

        if (window.user.is_hxt_viewer) {
            desktop_body_cards.push(HuskyExperienceCard);
            }

        if (window.user.student ||
            window.user.instructor ||
            window.user.employee) {
            desktop_body_cards.push(OutageCard);
        }

        if (window.user.student) {
            desktop_body_cards.push(GradeCard);
            desktop_body_cards.push(FutureQuarterCardA);
            desktop_body_cards.push(ThankYouCard);
            desktop_body_cards.push(ToRegisterCard);
            desktop_body_cards.push(RegStatusCard);
            desktop_body_cards.push(SummerEFSCard);
            desktop_body_cards.push(SummerRegStatusCardA);
            desktop_body_cards.push(CriticalInfoCard);
            desktop_body_cards.push(InternationalStuCard);
        }

        if (window.user.instructor) {
            desktop_body_cards.push(SummaryScheduleCard);
        }

        if (window.user.registered_stud || window.user.instructor) {
            desktop_body_cards.push(VisualScheduleCard);
        }

        if (window.user.student) {
            desktop_body_cards.push(TextbookCard);
        }

        if (window.user.instructor) {
            desktop_body_cards.push(FutureSummaryScheduleCard);
        }

        if (window.user.student) {
            desktop_body_cards.push(FutureQuarterCard1);
            desktop_body_cards.push(SummerRegStatusCard1);
        }
        if (window.user.applicant) {
            desktop_body_cards.push(SeattleApplicationCard);
            // desktop_body_cards.push(BothellApplicationCard);
            desktop_body_cards.push(TacomaApplicationCard);
        }

        if (window.user.intl_stud) {
            desktop_body_cards.push(IntlStudCard);
        }

        if(window.user.employee &&
           !window.user.student &&
           !window.user.instructor||
           window.user.retiree ||
           window.user.past_employee) {
            desktop_body_cards.push(HRPayrollCard);
        }

        if(window.user.retiree) {
            desktop_body_cards.push(RetireAssoCard);
        }

        if(window.user.past_stud) {
            desktop_body_cards.push(TranscriptsCard);
        }

        if (window.user.no_1st_class_affi) {
            desktop_body_cards.push(ContinuingEducationCard);
            desktop_body_cards.push(UwnetidCard);
        }

        if(window.user.alumni) {
            desktop_body_cards.push(AlumniCard);
        }

        // Always show these cards last
        desktop_body_cards.push(ResourcesCard, ResourcesExploreCard);
        return desktop_body_cards;
    },

    _get_desktop_sidebar_cards: function() {
        return [QuickLinksCard,
                AcadCalSnippet,
                EventsCard
               ];
    },

    _load_mobile_cards: function() {
        Landing._reset_content_divs();
        Cards.load_cards_in_order(Landing._get_mobile_cards(),
                                  $("#landing_content_cards"));
    },

    _get_mobile_cards: function() {
        var mobile_cards = [];
        if (window.user.is_hxt_viewer) {
            mobile_cards.push(HuskyExperienceCard);
        }

        if (window.user.applicant && !window.user.registered_stud) {
            mobile_cards.push(SeattleApplicationCard);
            // mobile_cards.push(BothellApplicationCard);
            mobile_cards.push(TacomaApplicationCard);
        }

        mobile_cards.push(QuickLinksCard);

        if (window.user.student ||
            window.user.instructor ||
            window.user.employee) {
            mobile_cards.push(OutageCard);
        }
        if (window.user.student) {
            mobile_cards.push(GradeCard);
            mobile_cards.push(FutureQuarterCardA);
            mobile_cards.push(ThankYouCard);
            mobile_cards.push(ToRegisterCard);
            mobile_cards.push(RegStatusCard);
            mobile_cards.push(SummerEFSCard);
            mobile_cards.push(SummerRegStatusCardA);
            mobile_cards.push(CriticalInfoCard);
            mobile_cards.push(InternationalStuCard);
        }
        if (window.user.instructor) {
            mobile_cards.push(SummaryScheduleCard);
            mobile_cards.push(FutureSummaryScheduleCard);
        }

        if (window.user.registered_stud || window.user.instructor) {
            mobile_cards.push(VisualScheduleCard);
        }
        if (window.user.student) {
            mobile_cards.push(TextbookCard);
            mobile_cards.push(FutureQuarterCard1);
            mobile_cards.push(SummerRegStatusCard1);
        }
        mobile_cards.push(AcadCalSnippet);
        mobile_cards.push(EventsCard);

        if (window.user.intl_stud) {
            mobile_cards.push(IntlStudCard);
        }

        if(window.user.employee &&
           !window.user.student &&
           !window.user.instructor &&
           !window.user.applicant ||
           window.user.retiree ||
           window.user.past_employee) {
            mobile_cards.push(HRPayrollCard);
        }

        if(window.user.retiree) {
            mobile_cards.push(RetireAssoCard);
        }

        if(window.user.past_stud) {
            mobile_cards.push(TranscriptsCard);
        }

        if (window.user.no_1st_class_affi) {
            mobile_cards.push(ContinuingEducationCard);
            mobile_cards.push(UwnetidCard);
        }

        if(window.user.alumni) {
            mobile_cards.push(AlumniCard);
        }
        // Always show these cards last
        mobile_cards.push(ResourcesCard, ResourcesExploreCard);
        return mobile_cards;
    },

    _reset_content_divs: function() {
        // Reset all the multiple resourse card render records
        // needed on every page refresh MUWM-3803
        resetCardRenderCalled();
        $("#landing_content_cards").html('');
        $("#landing_accounts_cards").html('');
    }

};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.Landing = Landing;
