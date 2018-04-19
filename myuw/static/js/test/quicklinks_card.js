var Global = require("./global.js");

describe('QuickLinksCard', function(){
    describe("Profile help links card", function() {
        before(function () {
            var render_id = 'render_links_card';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/quicklinks.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/quicklinks.html'
                ]
            });

            QuickLinksCard.dom_target = $('#' + render_id);
        });

        it("render links", function() {
            window.quicklink_data = {
                default_links: [
                    {url: "http://canvas.uw.edu/",
                     label: "Canvas LMS"},
                    {url: "https://myplan.uw.edu",
                     label: "MyPlan"}
                ],
                popular_links: [
                    {added: false,
                     id: "8",
                     url: "https://itconnect.uw.edu",
                     label: "IT Connect"},
                    {added: false,
                     id: "9",
                     url: "http://hr.uw.edu/jobs/",
                     label: "UW Jobs"},
                    {added: false,
                     id: "15",
                     url: "http://search.lib.uw.edu/account",
                     label: "Your Library Account"}
                ],
                recent_links: [
                    {added: false,
                     id: "1",
                     url: "https://notify.uw.edu/",
                     label: "Notify.UW"}
                ],
                custom_links: [
                    {id: "83",
                     url: "https://wiki.cac.washington.edu/",
                     label: "Wiki"},
                    {id: "130",
                     url: "https://www.washington.edu/transportation/",
                     label: "Parking"}
                ],
            };
            QuickLinksCard.render_init();
            assert.equal(QuickLinksCard.dom_target.find('.myuw-qlinks-item').length, 8);

            // default_links
            assert.equal(QuickLinksCard.dom_target.find('.myuw-qlinks-item')[0].innerHTML, '<a href="http://canvas.uw.edu/" title="Canvas LMS" data-notrack="" target="_blank"><span>Canvas LMS</span></a>');
            assert.ok(QuickLinksCard.dom_target.find('.link-controls')[0].innerHTML.includes("Remove Canvas LMS link from Quick Links list"))

            assert.equal(QuickLinksCard.dom_target.find('.myuw-qlinks-item')[1].innerHTML, '<a href="https://myplan.uw.edu" title="MyPlan" data-notrack="" target="_blank"><span>MyPlan</span></a>');

            // custom_links
            assert.ok(QuickLinksCard.dom_target.find('.myuw-qlinks-item')[2].innerHTML.includes("custom-link-83"));
            assert.ok(QuickLinksCard.dom_target.find('.myuw-qlinks-item')[3].innerHTML.includes("custom-link-130"));
            assert.ok(QuickLinksCard.dom_target.find('.link-controls')[3].innerHTML.includes("edit-link"))
            assert.ok(QuickLinksCard.dom_target.find('.link-controls')[3].innerHTML.includes("remove-link"))

            // recent_links
            assert.equal(QuickLinksCard.dom_target.find('.myuw-qlinks-item')[4].innerHTML, '<a href="https://notify.uw.edu/" title="Notify.UW" target="_blank"><span>Notify.UW</span></a>');
            assert.ok(QuickLinksCard.dom_target.find('.link-controls')[4].innerHTML.includes("Save Notify.UW link to your Quick Links list"))
            
            // popular_links
            assert.equal(QuickLinksCard.dom_target.find('.myuw-qlinks-item')[5].innerHTML, '<a href="https://itconnect.uw.edu" title="IT Connect" target="_blank"><span>IT Connect</span></a>');
            assert.ok(QuickLinksCard.dom_target.find('.link-controls')[5].innerHTML.includes("Save IT Connect link to your Quick Links list"))

            assert.equal(QuickLinksCard.dom_target.find('.myuw-qlinks-item')[6].innerHTML, '<a href="http://hr.uw.edu/jobs/" title="UW Jobs" target="_blank"><span>UW Jobs</span></a>');
            assert.equal(QuickLinksCard.dom_target.find('.myuw-qlinks-item')[7].innerHTML, '<a href="http://search.lib.uw.edu/account" title="Your Library Account" target="_blank"><span>Your Library Account</span></a>');
        });
    });
});
