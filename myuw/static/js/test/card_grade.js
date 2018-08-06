var Global = require("./global.js");

describe('GradeCard', function(){

    before(function () {
        var render_id = 'GradeCard';

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/card/grade.js"
            ],
            templates: [
                'myuw/templates/handlebars/card/grade.html'
            ]
        });

        GradeCard.dom_target = $('#' + render_id);
    });

    beforeEach(function (){
        window.page = "academics";
        Global.Environment.ajax_stub({
            '/api/v1/schedule/current': 'api/v1/schedule/javerage_2013_spring.json',
        });
    });

    afterEach(function(){
        Global.Environment.ajax_stub_restore();
    });

    it("Not render card if not in display window", function() {
        window.card_display_dates = {};
        GradeCard.render_init();
        assert.equal(GradeCard.dom_target.find('h3').length, 0);
    });

    it("Render card for javerage", function() {
        window.card_display_dates = {
            "system_date": '2013-06-17 00:01',
            "is_after_last_day_of_classes": true,
            "is_summer": false
        };
        GradeCard.render_init();
        assert.equal(GradeCard.dom_target.find('h3').length, 1);
        assert.equal(GradeCard.dom_target.find('h4').length, 1);
        assert.ok(GradeCard.dom_target.find('h3')[0].innerHTML, 'Final Grades');

        assert.equal(GradeCard.dom_target.find('li').length, 6);
        assert.equal(GradeCard.dom_target.find('span[class="card-badge-value pull-right"]').length, 3);

        assert.equal(GradeCard.dom_target.find('a[href="https://sdb.admin.uw.edu/sisStudents/uwnetid/grades.aspx"]').length, 1);
        assert.equal(GradeCard.dom_target.find('a[href="https://myplan.uw.edu/audit/login/netid?rd=/student/myplan/dars"]').length, 1);
        assert.equal(GradeCard.dom_target.find('a[href="https://sdb.admin.uw.edu/students/uwnetid/unofficial.asp"]').length, 1);
    });
});
