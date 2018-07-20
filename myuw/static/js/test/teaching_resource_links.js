var Global = require("./global.js");

describe('TeachingResourceLinksCard', function(){
    describe("Teaching resource links card", function() {
        before(function () {
            var render_id = 'render_links_card';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/teaching_resources.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/teaching_resources.html'
                ]
            });

            TeachingResourcesCard.dom_target = $('#' + render_id);
        });
        it("render seattle links", function() {
            window.user.seattle_emp = true;
            window.user.tacoma_emp = false;
            window.user.bothell_emp = false;
            TeachingResourcesCard.render_init();
            assert.equal(TeachingResourcesCard.dom_target.find('a[href="http://www2.bookstore.washington.edu/textsys/TextReqLogin.taf?school=uwmain"]').length, 1);
            assert.equal(TeachingResourcesCard.dom_target.find('a[href="https://uw.iasystem.org/faculty"]').length, 1);
        });
        it("render tacoma links", function() {
            window.user.seattle_emp = false;
            window.user.tacoma_emp = true;
            window.user.bothell_emp = false;
            TeachingResourcesCard.render_init();
            assert.equal(TeachingResourcesCard.dom_target.find('a[href="http://www2.bookstore.washington.edu/textsys/TextReqLogin.taf?school=uwtacoma"]').length, 1);
            assert.equal(TeachingResourcesCard.dom_target.find('a[href="https://uwt.iasystem.org/faculty"]').length, 1);
        });
        it("render bothell links", function() {
            window.user.seattle_emp = false;
            window.user.tacoma_emp = false;
            window.user.bothell_emp = true;
            TeachingResourcesCard.render_init();
            assert.equal(TeachingResourcesCard.dom_target.find('a[href="http://www2.bookstore.washington.edu/textsys/TextReqLogin.taf?school=uwbothell"]').length, 1);
            assert.equal(TeachingResourcesCard.dom_target.find('a[href="https://uwb.iasystem.org/faculty"]').length, 1);
        });
    });
});
