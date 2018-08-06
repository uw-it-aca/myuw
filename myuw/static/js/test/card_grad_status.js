var Global = require("./global.js");

describe('GradStatusCard', function(){

    before(function () {
        var render_id = 'GradStatusCard';

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/card/grad_status.js"
            ],
            templates: [
                'myuw/templates/handlebars/card/grad_status.html'
            ]
        });

        GradStatusCard.dom_target = $('#' + render_id);
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
        GradStatusCard.render_init();
        assert.equal(GradStatusCard.dom_target.find('h3').length, 0);
    });

    it("Render card for graduate student", function() {
        window.user.grad = true;
        GradStatusCard.render_init();
        assert.equal(GradStatusCard.dom_target.find('h3').length, 1);
        assert.equal(GradStatusCard.dom_target.find('h4').length, 3);
        assert.ok(GradStatusCard.dom_target.find('h3')[0].innerHTML, 'Graduate Request Status');
        assert.ok(GradStatusCard.dom_target.find('h4')[0].innerHTML, 'Petition Requests'); 
        assert.ok(GradStatusCard.dom_target.find('h4')[1].innerHTML, 'Leave Requests'); 
        assert.ok(GradStatusCard.dom_target.find('h4')[2].innerHTML, 'Degree and Exam Requests'); 
        assert.equal(GradStatusCard.dom_target.find('ul.card_list').length, 3);
        assert.equal(GradStatusCard.dom_target.find('li').length, 28);
        assert.equal(GradStatusCard.dom_target.find('span.card-badge-label').length, 21);
    });
});
