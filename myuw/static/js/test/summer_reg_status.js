var Global = require("./global.js");

describe('Summer Reg Card A', function(){
    before(function (done) {
        var render_id = 'SummerRegCardELM';

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/card/reg_status.js",
                "myuw/static/js/card/summer_reg_status.js",
                "myuw/static/js/notices.js"
            ],
            templates: [
                "myuw/templates/handlebars/card/reg_status.html",
                "myuw/templates/handlebars/card/registration/est_reg_date.html",
                "myuw/templates/handlebars/card/registration/reg_resources.html"
            ]
        });

        $('body').append($('<div/>', { 'id': "SummerRegStatusCardA" }));
        //
        //window.enabled_features = { 'instructor_schedule': false };
        //
        Global.Environment.ajax_stub({
            '/api/v1/profile/': '/api/v1/profile/index-javerage.json',
            '/api/v1/notices/': '/api/v1/notices/javerage-summer-reg.json',
            '/api/v1/oquarters/': '/api/v1/oquarters/javerage-no-summer-reg.json',
            '/api/v1/myplan/2013/Summer': '/api/v1/myplan/javerage-2013-spring.json',
        });

        $(window).on("myuw:card_load", function () {
            done();
        });
        window.card_display_dates = {};
        window.card_display_dates.is_after_start_of_summer_reg_display_periodA = true;
        window.card_display_dates.is_after_start_of_summer_reg_display_period1 = false;

        Handlebars.registerPartial("notice_est_reg_date",
                                   $("#notice_est_reg_date_tmpl").html());
        Handlebars.registerPartial("reg_resources",
                                   $("#reg_resources_tmpl").html());

        SummerRegStatusCard.dom_target = $('#' + render_id);
        SummerRegStatusCard.render_init();
    });
    it("Should render card", function() {
        assert.equal(SummerRegStatusCard.dom_target.find('#RegStatusCard').length, 1);
        assert.equal(SummerRegStatusCard.dom_target.find('#RegStatusCard').attr("data-identifier"), "Summer2013");
        assert.equal(SummerRegStatusCard.label, 'summerA')
    });
    after(function () {
        Global.Environment.ajax_stub_restore();
    });
});

describe('Summer Reg Card B', function(){
    before(function (done) {
        var render_id = 'SummerRegCardELM';

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/card/reg_status.js",
                "myuw/static/js/card/summer_reg_status.js",
                "myuw/static/js/notices.js"
            ],
            templates: [
                "myuw/templates/handlebars/card/reg_status.html",
                "myuw/templates/handlebars/card/registration/est_reg_date.html",
                "myuw/templates/handlebars/card/registration/reg_resources.html"
            ]
        });

        $('body').append($('<div/>', { 'id': "SummerRegStatusCard1" }));
        //
        //window.enabled_features = { 'instructor_schedule': false };
        //
        Global.Environment.ajax_stub({
            '/api/v1/profile/': '/api/v1/profile/index-javerage.json',
            '/api/v1/notices/': '/api/v1/notices/javerage-summer-reg.json',
            '/api/v1/oquarters/': '/api/v1/oquarters/javerage-no-summer-reg.json',
            '/api/v1/myplan/2013/Summer': '/api/v1/myplan/javerage-2013-spring.json',
        });

        $(window).on("myuw:card_load", function () {
            done();
        });
        window.card_display_dates = {};
        window.card_display_dates.is_after_start_of_summer_reg_display_periodA = false;
        window.card_display_dates.is_after_start_of_summer_reg_display_period1 = true;

        Handlebars.registerPartial("notice_est_reg_date",
                                   $("#notice_est_reg_date_tmpl").html());
        Handlebars.registerPartial("reg_resources",
                                   $("#reg_resources_tmpl").html());

        SummerRegStatusCard.dom_target = $('#' + render_id);
        SummerRegStatusCard.render_init();
    });
    it("Should render card", function() {
        assert.equal(SummerRegStatusCard.dom_target.find('#RegStatusCard').length, 1);
        assert.equal(SummerRegStatusCard.dom_target.find('#RegStatusCard').attr("data-identifier"), "Summer2013");
        assert.equal(SummerRegStatusCard.label, 'summer1')
    });
    after(function () {
        Global.Environment.ajax_stub_restore();
    });
});