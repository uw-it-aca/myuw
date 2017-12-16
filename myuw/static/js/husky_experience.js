var HuskyExperiencePage = {
    is_desktop: undefined,
    article_id: undefined,

    render: function() {
        showLoading();
        HuskyExperiencePage.make_html();
        var article_id = getUrlParameter('article');
        if(article_id !== null && article_id.length > 0){
            HuskyExperiencePage.article_id = article_id;
            WSData.fetch_hx_toolkit_msg_data(article_id,
                                              HuskyExperiencePage.make_detail_html,
                                              HuskyExperiencePage.render_error);
            HuskyExperiencePage.make_detail_html(article_id);
        } else {
            WSData.fetch_hx_toolkit_list_data(HuskyExperiencePage.make_summary_html,
                                              HuskyExperiencePage.render_error);
        }
    },

    make_html: function () {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var HuskyExperience_source = $("#husky_experience_page").html();
        var template = Handlebars.compile(HuskyExperience_source);

        $("#main-content").html(template());

        // Set initial display state
        HuskyExperiencePage.is_desktop = get_is_desktop();

    },

    make_detail_html: function () {
        var article_html = WSData.hx_toolkit_msg_data(HuskyExperiencePage.article_id);
        $('html,body').animate({scrollTop: 0}, 'fast');
        var source = $("#husky_experience_detail").html();
        var template = Handlebars.compile(source);
        var data = {article_html: article_html};

        $("#main-content").html(template(data));

        // Set initial display state
        HuskyExperiencePage.is_desktop = get_is_desktop();

    },

    make_summary_html: function () {
        var summary_data = WSData.hx_toolkit_list_data();
        $('html,body').animate({scrollTop: 0}, 'fast');
        var source = $("#husky_experience_page").html();
        var template = Handlebars.compile(source);

        var data = {};
        data['know-yourself'] = [{slug: "know-yourself-week-1", title: "Know Yourself Week 1"}];

        var rendered = template({categories: summary_data});

        $("#main-content").html(rendered);
        return ''
    },

    _reset_content_divs: function() {
        $("#huskyx_content_cards").html('');
        $("#huskyx_sidebar_cards").html('');
    }
};
