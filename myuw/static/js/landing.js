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
        var desktop_body_cards = [
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
            TacomaApplicationCard,
            WelcomeCard
        ];

        if(!window.user.student &&
           !window.user.instructor &&
           !window.user.applicant) {

            if(window.user.employee ||
               window.user.clinician ||
               window.user.past_employee) {
                desktop_body_cards.push(HRPayrollCard);
            }

            if(window.user.retiree) {
                desktop_body_cards.push(RetireAssoCard);
            }

            if(window.user.past_stud) {
                desktop_body_cards.push(TranscriptsCard);
            }

            desktop_body_cards.push(ContinuingEducationCard);

            if(window.user.past_stud ||
               window.user.past_employee) {
                desktop_body_cards.push(UwnetidCard);
            }

            if(window.user.alumni) {
                desktop_body_cards.push(AlumniCard);
            }
        }

        var desktop_sidebar_cards = [
            QuickLinksCard,
            AcadCalSnippet,
            EventsCard
        ];
        Cards.load_cards_in_order(desktop_body_cards, $("#landing_content_cards"));
        Cards.load_cards_in_order(desktop_sidebar_cards, $("#landing_accounts_cards"));
    },

    _load_mobile_cards: function() {
        Landing._reset_content_divs();
        var mobile_cards = [
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
            EventsCard,
            WelcomeCard
        ];

        if(!window.user.student &&
           !window.user.instructor &&
           !window.user.applicant) {

            if(window.user.employee ||
               window.user.clinician ||
               window.user.past_employee) {
                desktop_body_cards.push(HRPayrollCard);
            }

            if(window.user.retiree) {
                desktop_body_cards.push(RetireAssoCard);
            }

            if(window.user.past_stud) {
                desktop_body_cards.push(TranscriptsCard);
            }

            desktop_body_cards.push(ContinuingEducationCard);

            if(window.user.past_stud ||
               window.user.past_employee) {
                desktop_body_cards.push(UwnetidCard);
            }

            if(window.user.alumni) {
                desktop_body_cards.push(AlumniCard);
            }
        }

        Cards.load_cards_in_order(mobile_cards, $("#landing_content_cards"));
    },

    _reset_content_divs: function() {
        // Reset all the multiple resourse card render records
        // needed on every page refresh MUWM-3803
        resetCardRenderCalled();
        $("#landing_content_cards").html('');
        $("#landing_accounts_cards").html('');
    }

};
