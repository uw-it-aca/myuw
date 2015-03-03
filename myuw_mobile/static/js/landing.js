var Landing = {
    render: function() {        
        //Navbar.render_navbar();
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
        CalendarBanner.render_init($("#calendar_banner_location"));
        var cards = [
                     FinalExamCard,           
                     GradeCard,
                     FutureQuarterCardA,
                     RegStatusCard,
                     SummerRegStatusCardA,
                     VisualScheduleCard,
                     TextbookCard,
                     CourseCard,
                     HfsCard,
                     TuitionCard,
                     LibraryCard,
                     AcademicCard,
                     FutureQuarterCard1,
                     SummerRegStatusCard1
                    ];
        
        Cards.load_cards_in_order(cards, $("#landing_content"));
                
    }
};
