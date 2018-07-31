var Global = require("./global.js");

describe('InterStudentCard', function(){

    before(function () {
        var render_id = 'InterStudentCard';

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/card/international_student.js"
            ],
            templates: [
                'myuw/templates/handlebars/card/international_student.html'
            ]
        });

        InterStudentCard.dom_target = $('#' + render_id);
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
        InterStudentCard.render_init();
        assert.equal(InterStudentCard.dom_target.find('h3').length, 0);
    });

    it("Render card for Seattle intl students", function() {
        window.user.f1 = true;
        window.user.seattle = true;
        InterStudentCard.render_init();

        assert.equal(InterStudentCard.dom_target.find('h3').length, 1);
        assert.ok(InterStudentCard.dom_target.find('h3')[0].innerHTML.indexOf('International Student')>0);
        assert.equal(InterStudentCard.dom_target.find('h4').length, 3);
        assert.equal(InterStudentCard.dom_target.find('li').length, 9);
        assert.equal(InterStudentCard.dom_target.find('a[href="https://iss.washington.edu/regulations/f1/"]').length, 1);
        assert.equal(InterStudentCard.dom_target.find('a[href="http://www.fiuts.org/events"]').length, 1);
    });

    it("Render for bothell J1 students", function() {
        window.user.j1 = true;
        window.user.bothell = true;
        InterStudentCard.render_init();
        assert.equal(InterStudentCard.dom_target.find('li').length, 8);
        assert.equal(InterStudentCard.dom_target.find('a[href="http://www.uwb.edu/cie/current-students/travel"]').length, 1);
        assert.equal(InterStudentCard.dom_target.find('a[href="https://www.uwb.edu/cie/current-students/immigration-documents"]').length, 1);
    });

    it("Render for bothell J1 students", function() {
        window.user.tacoma = true;
        InterStudentCard.render_init();
        assert.equal(InterStudentCard.dom_target.find('ul.unstyled-list').length, 2);
        assert.equal(InterStudentCard.dom_target.find('li').length, 6);
        assert.equal(InterStudentCard.dom_target.find('a[href="http://www.tacoma.uw.edu/iss/maintaining-f-1-status"]').length, 1);
        assert.equal(InterStudentCard.dom_target.find('a[href="http://www.tacoma.uw.edu/teaching-learning-center/teaching-learning-center"]').length, 1);
    });

});
