var Landing = {
    is_desktop: undefined,

    render: function() {
        showLoading();
        CommonLoading.render_init();
        Landing.make_html();
    },

    make_html: function () {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var landing_source = $("#landing").html();
        var template = Handlebars.compile(landing_source);

        $("#main-content").html(template());

        NoticeBanner.render_init($("#notice_banner_location"));

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
            ThriveCard,
            GradeCard,
            FutureQuarterCardA,
            ThankYouCard,
            ToRegisterCard,
            RegStatusCard,
            SummerEFSCard,
            SummerRegStatusCardA,
            CriticalInfoCard,
            InternationalStuCard,
            VisualScheduleCard,
            TextbookCard,
            FutureQuarterCard1,
            SummerRegStatusCard1
        ];
        var desktop_sidebar_cards = [
            QuickLinksCard,
            EmpFacStudentCard,
            EventsCard
        ];
        // Add in outage card if we can't get the SWS/term resource
        if(window.webservice_outage){
            desktop_body_cards.unshift(OutageCard);
        }
        Cards.load_cards_in_order(desktop_body_cards, $("#landing_content_cards"));
        Cards.load_cards_in_order(desktop_sidebar_cards, $("#landing_accounts_cards"));
    },

    _load_mobile_cards: function() {
        Landing._reset_content_divs();
        var mobile_cards = [
            QuickLinksCard,
            ThriveCard,
            GradeCard,
            FutureQuarterCardA,
            ThankYouCard,
            ToRegisterCard,
            RegStatusCard,
            SummerEFSCard,
            SummerRegStatusCardA,
            CriticalInfoCard,
            InternationalStuCard,
            VisualScheduleCard,
            TextbookCard,
            FutureQuarterCard1,
            SummerRegStatusCard1,
            EmpFacStudentCard,
            EventsCard
        ];
        // Add in outage card if we can't get the SWS/term resource
        if(window.webservice_outage){
            mobile_cards.unshift(OutageCard);
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
