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
        Landing.is_desktop = Landing.get_is_desktop();

        // Monitor for viewport changes and reorder cards if needed
        $(window).resize(function(){
            if (Landing.is_desktop !== Landing.get_is_desktop()){
                Landing.load_cards_for_viewport();
                Landing.is_desktop = Landing.get_is_desktop();
            }
        });
    },

    get_is_desktop: function() {
        var mobile_cutoff_width = 992;
        var viewport_width = $(window).width();
        if (viewport_width >= mobile_cutoff_width) {
            return true;
        } else {
            return false;
        }

    },

    load_cards_for_viewport: function() {
        if (Landing.get_is_desktop()) {
            Landing._load_desktop_cards();
        } else {
            Landing._load_mobile_cards();
        }
    },
    _load_desktop_cards: function() {
        Landing._reset_content_divs();
        var desktop_body_cards = [
            FinalExamCard,
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
            CourseCard,
            FutureQuarterCard1,
            SummerRegStatusCard1
        ];
        var desktop_sidebar_cards = [
            EmpFacStudentCard,
            HfsCard,
            TuitionCard,
            LibraryCard,
            EventsCard
        ];
        Cards.load_cards_in_order(desktop_body_cards, $("#landing_content_cards"));
        Cards.load_cards_in_order(desktop_sidebar_cards, $("#landing_accounts_cards"));
        CalendarBanner.render_init($("#calendar_banner_location_desktop"));
    },

    _load_mobile_cards: function() {
        Landing._reset_content_divs();
        var mobile_cards = [
            EmpFacStudentCard,
            FinalExamCard,
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
            CourseCard,
            HfsCard,
            TuitionCard,
            LibraryCard,
            EventsCard,
            FutureQuarterCard1,
            SummerRegStatusCard1
        ];
        Cards.load_cards_in_order(mobile_cards, $("#landing_content_cards"));
        CalendarBanner.render_init($("#calendar_banner_location_mobile"));
    },

    _reset_content_divs: function() {
        $("#landing_content_cards").html('');
        $("#landing_accounts_cards").html('');
        $("#calendar_banner_location_desktop").html('');
        $("#calendar_banner_location_mobile").html('');
    }

};
