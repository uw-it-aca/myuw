var Global = require("./global.js");

describe('QuickLinksCard', function(){

    before(function () {
        var render_id = 'render_quick_links_card';
        var spy_add_link;

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/card/error.js",
                "myuw/static/js/card/quicklinks.js"
            ],
            templates: [
                'myuw/templates/handlebars/card/error.html',
                'myuw/templates/handlebars/card/quicklinks.html'
            ]
        });
        QuickLinksCard.dom_target = $('#' + render_id);
    });

    beforeEach(function (){
        Global.Environment.ajax_stub({
            '/api/v1/link/': '/api/v1/link/javerage.json',
        });
        QuickLinksCard.render_init();
    });

    afterEach(function(){
        Global.Environment.ajax_stub_restore();
    });

    it("Test render links", function() {
        assert.equal(QuickLinksCard.dom_target.find('.myuw-qlinks-item').length, 8);

        // default_links
        assert(QuickLinksCard.dom_target.find('.myuw-qlinks-item')[0].innerHTML.includes('<a href="http://canvas.uw.edu/"'));
        assert(QuickLinksCard.dom_target.find('.link-controls')[0].innerHTML.includes("Remove Canvas LMS link from Quick Links list"));

        assert(QuickLinksCard.dom_target.find('.myuw-qlinks-item')[1].innerHTML.includes('<a href="https://myplan.uw.edu"'));

        // custom_links
        assert(QuickLinksCard.dom_target.find('.myuw-qlinks-item')[2].innerHTML.includes("custom-link-83"));
        assert(QuickLinksCard.dom_target.find('.myuw-qlinks-item')[3].innerHTML.includes("custom-link-130"));
        assert(QuickLinksCard.dom_target.find('.link-controls')[3].innerHTML.includes("edit-link"));
        assert(QuickLinksCard.dom_target.find('.link-controls')[3].innerHTML.includes("remove-link"));

        // recent_links
        assert(QuickLinksCard.dom_target.find('.myuw-qlinks-item')[4].innerHTML.includes('<a href="https://notify.uw.edu/"'));
        assert(QuickLinksCard.dom_target.find('.link-controls')[4].innerHTML.includes("Save Notify.UW link to your Quick Links list"));

        // popular_links
        assert(QuickLinksCard.dom_target.find('.myuw-qlinks-item')[5].innerHTML.includes('<a href="https://itconnect.uw.edu"'));
        assert(QuickLinksCard.dom_target.find('.link-controls')[5].innerHTML.includes("Save IT Connect link to your Quick Links list"));

        assert(QuickLinksCard.dom_target.find('.myuw-qlinks-item')[6].innerHTML.includes('<a href="http://hr.uw.edu/jobs/"'));
        assert(QuickLinksCard.dom_target.find('.myuw-qlinks-item')[7].innerHTML.includes('<a href="http://search.lib.uw.edu/account"'));
    });

    it("Test edit custom link show disclosure", function() {
        // the div is hidden before clicking edit
        var style = QuickLinksCard.dom_target.find('#custom-link-edit')[0].getAttribute("style");
        assert.equal(style, "display: none;");
        // the edit link
        var a = QuickLinksCard.dom_target.find('#custom-link-edit-control-83');
        a.trigger('click');
        // the div is displayed
        var style = QuickLinksCard.dom_target.find('#custom-link-edit')[0].getAttribute("style");
        assert.equal(style, 'left: 0px; top: 20px;');
    });

    it("Test remove a default link", function() {
        spy_add_link = sinon.spy(QuickLinksCard, "_add_link");
        var a = QuickLinksCard.dom_target.find('#rm-def-link-0');
        try {
            a.trigger('click');
        } catch (e) {
            assert.equal(e.name, "TypeError");
        } finally {
            spy_add_link.restore();
            assert.equal(spy_add_link.callCount, 1);
        }
    });
});
