var Landing = {
    render: function() {
        //Navbar.render_navbar();
        showLoading();
        UwEmail.render_init();
        
        // wait 1/2 second before loading cards
        setTimeout(function() {
              Landing.make_html();
        }, 500);
        
    },

    make_html: function () {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var landing_source = $("#landing").html();
        var template = Handlebars.compile(landing_source);
        
        $("#main-content").html(template());

        NoticeBanner.render_init($("#notice_banner_location"));
        var cards = [FutureQuarterCard,
                     VisualScheduleCard,
                     CourseCard,
                     HfsCard,
                     TuitionCard,
                     LibraryCard,
                     RegStatusCard];
        
        // hide the loading message before loading content           
        $("#app_loading").hide();
        
        Cards.load_cards_in_order(cards, $("#landing_content"));
 
    }
};
