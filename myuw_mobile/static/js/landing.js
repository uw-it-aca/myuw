var Landing = {
    render: function() {
        showLoading();
        Landing.make_html();
    },

    make_html: function() {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var cards = [RegStatusCard,
                     VisualScheduleCard,
                     CourseCard,
                     TuitionCard,
                     PCETuitionCard,
                     TextbookCard,
                     HfsCard,
                     LibraryCard];

        Cards.load_cards_in_order(cards, $("#main-content"));
    },

};
