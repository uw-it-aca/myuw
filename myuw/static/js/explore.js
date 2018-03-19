var Explore = {

    render: function() {
        showLoading();
        Explore.make_html();
    },

    make_html: function () {
        $('html,body').animate({scrollTop: 0}, 'fast');
        // var source = $("#explore_page").html();
        // var template = Handlebars.compile(source);
        $("#main-content").html("foo");
    }

};
