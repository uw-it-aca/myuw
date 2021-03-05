var Global = require("./global.js");

describe('IntlStudCard', function(){

    before(function () {
        var render_id = 'IntlStudCard';

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/card/international_student.js"
            ],
            templates: [
                'myuw/templates/handlebars/card/international/international_student.html',
                'myuw/templates/handlebars/card/international/bothell_international.html',
                'myuw/templates/handlebars/card/international/seattle_international.html',
                'myuw/templates/handlebars/card/international/tacoma_international.html'
            ]
        });

        IntlStudCard.dom_target = $('#' + render_id);
    });

    beforeEach(function (){
        window.page = "home";
        window.user.f1 = false;
        window.user.j1 = false;
        window.user.intl_stud = true;
        window.user.seattle = false;
        window.user.bothell = false;
        window.user.tacoma = false;
        });

    afterEach(function(){
    });

    it("Not render card if not intl students", function() {
        window.user.intl_stud = false;
        IntlStudCard.render_init();
        assert.equal(IntlStudCard.dom_target.find('h3').length, 0);
    });

    it("Render card for Seattle intl students", function() {
        window.user.f1 = true;
        window.user.seattle = true;
        IntlStudCard.render_init();

        assert.equal(IntlStudCard.dom_target.find('h3').length, 1);
        assert(IntlStudCard.dom_target.find('h3.myuw-card-title')[0].innerHTML.includes('International Student'));
        assert.equal(IntlStudCard.dom_target.find('h4').length, 3);
        assert.equal(IntlStudCard.dom_target.find('li').length, 10);
        assert.equal(IntlStudCard.dom_target.find('a[href="https://iss.washington.edu/regulations/f1/"]').length, 1);
        assert.equal(IntlStudCard.dom_target.find('a[href="http://www.fiuts.org/events"]').length, 1);
    });

    it("Render for bothell J1 students", function() {
        window.user.j1 = true;
        window.user.bothell = true;
        IntlStudCard.render_init();
        assert.equal(IntlStudCard.dom_target.find('li').length, 8);
        assert.equal(IntlStudCard.dom_target.find('a[href="http://www.uwb.edu/cie/current-students/travel"]').length, 1);
        assert.equal(IntlStudCard.dom_target.find('a[href="https://www.uwb.edu/cie/current-students/immigration-documents"]').length, 1);
    });

    it("Render for tacoma intl students", function() {
        window.user.tacoma = true;
        IntlStudCard.render_init();
        assert.equal(IntlStudCard.dom_target.find('ul.unstyled-list').length, 2);
        assert.equal(IntlStudCard.dom_target.find('li').length, 6);
        assert.equal(IntlStudCard.dom_target.find('a[href="http://www.tacoma.uw.edu/iss/maintaining-f-1-status"]').length, 1);
        assert.equal(IntlStudCard.dom_target.find('a[href="http://www.tacoma.uw.edu/teaching-learning-center/teaching-learning-center"]').length, 1);
    });

    it("Render for intl students wo campus", function() {
        IntlStudCard.render_init();
        assert.equal(IntlStudCard.dom_target.find('ul.unstyled-list').length, 7);
        assert.equal(IntlStudCard.dom_target.find('div.myuw-tab').length, 3);
        assert.equal(IntlStudCard.dom_target.find('div.intl_tab_content').length, 3);
        assert.equal(IntlStudCard.dom_target.find('a[href="https://iss.washington.edu/regulations/f1/"]').length, 1);
    });

});
