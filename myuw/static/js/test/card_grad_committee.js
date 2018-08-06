var Global = require("./global.js");

describe('GradCommitteeCard', function(){

    before(function () {
        var render_id = 'GradCommitteeCard';

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/card/grad_committee.js"
            ],
            templates: [
                'myuw/templates/handlebars/card/grad_committee.html'
            ]
        });

        GradCommitteeCard.dom_target = $('#' + render_id);
    });

    beforeEach(function (){
        window.page = "academics";
        Global.Environment.ajax_stub({
            '/api/v1/grad/': 'api/v1/grad/seagrad.json',
        });
    });

    afterEach(function(){
        Global.Environment.ajax_stub_restore();
    });

    it("Not render card if graduate student", function() {
        GradCommitteeCard.render_init();
        assert.equal(GradCommitteeCard.dom_target.find('h3').length, 0);
    });

    it("Render card for seagrad", function() {
        window.user.grad = true;
        GradCommitteeCard.render_init();
        assert.equal(GradCommitteeCard.dom_target.find('h3').length, 1);
        assert.equal(GradCommitteeCard.dom_target.find('h4').length, 3);
        assert.ok(GradCommitteeCard.dom_target.find('h3')[0].innerHTML, 'Your Committees');
        assert.ok(GradCommitteeCard.dom_target.find('h4')[0].innerHTML, 'Advisor'); 
        assert.ok(GradCommitteeCard.dom_target.find('h4')[1].innerHTML, "Master's Committee"); 
        assert.ok(GradCommitteeCard.dom_target.find('h4')[2].innerHTML, 'Doctoral Supervisory Committee'); 
        assert.equal(GradCommitteeCard.dom_target.find('li').length, 11);
        assert.equal(GradCommitteeCard.dom_target.find('a[href="http://www.grad.uw.edu/mygrad/student.htm"]').length, 1);
    });
});
