var Global = require("./global.js");

describe('TextbookCard', function(){
    before(function (done) {
        var render_id = 'TextbookCard';

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/textbooks.js",
                "myuw/static/js/card/textbook.js"
            ],
            templates: [
                "myuw/templates/handlebars/card/textbook.html"
            ]
        });

        window.enabled_features = { 'instructor_schedule': false };

        Global.Environment.ajax_stub({
            '/api/v1/schedule/2013,summer,a-term': '/api/v1/schedule/2013,summer,a-term',
            '/api/v1/book/2013,summer,a-term': '/api/v1/book/2013,summer,a-term'
        });

        $(window).on("myuw:card_load", function () {
            done();
        });

        TextbookCard.term = '2013,summer,a-term'
        TextbookCard.dom_target = $('#' + render_id);
        TextbookCard.render_init();
    });
    it("Should render card", function() {
        assert.equal(TextbookCard.dom_target.find('ul.textbooks-list').length, 1);
    });
    after(function () {
        Global.Environment.ajax_stub_restore();
    });
});
