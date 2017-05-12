var Global = require("./global.js");

describe('DirectoryInfoCard', function(){
    describe("directory info card", function() {
        before(function (done) {
            var render_id = 'dir_info';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/profile/directory_info.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/directory_info.html'
                ]
            });

            Global.Environment.ajax_stub('api/v1/directory/index.json');

            $(window).on("myuw:card_load", function () {
                done();
            });

            window.user.faculty = true;

            DirectoryInfoCard.dom_target = $('#' + render_id);
            DirectoryInfoCard.render_init();
        });
        it("Should render instructor card", function() {
            assert.equal($('span[property="telephone"]').html(), '(206) 555-1235');
        });
    });
});
