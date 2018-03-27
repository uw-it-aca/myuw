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
        var desktop_body_cards = [
            ResourcesCard,
            HuskyExperienceCard,
            ThriveCard,
            OutageCard,
            GradeCard,
            FutureQuarterCardA,
            ThankYouCard,
            ToRegisterCard,
            RegStatusCard,
            SummerEFSCard,
            SummerRegStatusCardA,
            CriticalInfoCard,
            InternationalStuCard,
            SummaryScheduleCard,
            VisualScheduleCard,
            TextbookCard,
            FutureSummaryScheduleCard,
            FutureQuarterCard1,
            SummerRegStatusCard1,
            SeattleApplicationCard,
            BothellApplicationCard,
            TacomaApplicationCard
        ];

        if(window.user.employee &&
           !window.user.student &&
           !window.user.instructor||
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
        var mobile_cards = [
            ResourcesCard,
            HuskyExperienceCard,
            SeattleApplicationCard,
            BothellApplicationCard,
            TacomaApplicationCard,
            QuickLinksCard,
            ThriveCard,
            OutageCard,
            GradeCard,
            FutureQuarterCardA,
            ThankYouCard,
            ToRegisterCard,
            RegStatusCard,
            SummerEFSCard,
            SummerRegStatusCardA,
            CriticalInfoCard,
            InternationalStuCard,
            SummaryScheduleCard,
            FutureSummaryScheduleCard,
            VisualScheduleCard,
            TextbookCard,
            FutureQuarterCard1,
            SummerRegStatusCard1,
            AcadCalSnippet,
            EventsCard
        ];

        if(window.user.employee &&
           !window.user.student &&
           !window.user.instructor &&
           !window.user.applicant ||
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
