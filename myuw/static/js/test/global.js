var path = require("path");
var fs = require("fs");
var assert = require("assert");
var sinon = require("sinon");

var Environment = {
    _stub: null,

    init: function (config) {
        /*
         * config object supports:
         *      user: myuw user object, template in user_state.html
         *      render_id: rendered object container id
         *      scripts: required javascript modules to include
         *      templates: template files used for rendering
         */
        if (!config) {
            config = {};
        }

        // create test document
        var jsdom = require('jsdom');
        const { JSDOM } = jsdom;
        var dom = new JSDOM('');

        // pull in supporting tools
        var $ = require('jquery')(dom.window);
        global.$ = $;
        global.window = dom.window;
        global.document = dom.window.document;
        global.assert = require("assert");
        global.moment = require("moment-timezone");
        global.sinon  = require("sinon");
        global.Handlebars = require("../../vendor/js/handlebars-v4.0.5.js");
        global.dom = dom;
        var HandlebarsHelpers = require("../handlebars-helpers.js");

        // set up client environment
        window.user = Environment._get_user(config);
        window.is_mobile = false;
        window.static_url = 'http://static/path';

        // default test term
        window.term = {};
        window.term.year = 2013;
        window.term.quarter = 'spring';
        window.term.first_day_quarter = 'Monday, April 1, 2013';
        window.term.last_day_instruction = 'Friday, June 7, 2013';

        if (config.hasOwnProperty('render_id')) {
            $('body').append($('<div/>', { 'id': config.render_id }));
        }

        // stub onload init routines
        window.RenderPage = function () {};
        global.Profile = { add_events: function () {} };
        global.Modal = { add_events: function () {} };
        global.LogUtils = {
            init_logging: function () {},
            cardLoaded: function(name, el) {
                $(window).trigger("myuw:card_load", [ name, el ])
            }
        };

        // pull in scripts
        Environment._load_script('myuw/static/js/myuw_m.js');
        Environment._load_script('myuw/static/js/ws_data.js');
        if (config.hasOwnProperty('scripts')) {
            $.each(config.scripts, function () {
                Environment._load_script(this.toString());
            });
        }

        // pull in templates
        if (config.hasOwnProperty('templates')) {
            $.each(config.templates, function () {
                Environment._load_template(this.toString());
            });
        }
    },
    _get_user: function (config) {
        var user;
        if (config.hasOwnProperty('user')) {
            user = config.user;
        } else {
            user = {
                alumni: false,
                applicant: false,
                bothell: false,
                bothell_emp: false,
                email_forward_icon: "",
                email_forward_title: "",
                email_forward_url: "",
                employee: false,
                faculty: false,
                instructor: false,
                fyp: false,
                aut_transfer: false,
                win_transfer: false,
                grad: false,
                netid: "bill",
                pce: false,
                seattle: true,
                seattle_emp: false,
                stud_employee: false,
                student: true,
                tacoma: false,
                tacoma_emp: false,
                undergrad: false,
                is_hxt_viewer: false,
                no_1st_class_affi: false,
                retiree: false,
                past_stud: false,
                past_employee: false,
                intl_stud: false,
            };
        }

        return user;
    },
    _abs_path: function (relative_path) {
        return path.join(__dirname, '../../../../', relative_path);
    },
    _json_from_file: function (json_data_file) {
        var json_dir = path.join('myuw/static/js/test/ajax', json_data_file);
        var json_file = Environment._abs_path(json_dir);
        return JSON.parse(fs.readFileSync(json_file));
    },
    ajax_stub: function (json_config) {
        if ($.type(json_config) === 'string') {
            var json_data = Environment._json_from_file(json_config)
            Environment._stub = sinon.stub($, 'ajax');
            Environment._stub.yieldsTo('success', json_data);
        } else {
            Environment._stub = sinon.stub($, 'ajax')
                .callsFake(function (conf) {
                    if (conf.url in json_config) {
                        var json_data = Environment._json_from_file(json_config[conf.url]);
                        conf.success.apply(null, [json_data]);
                    } else {
                        conf.error.apply(null, [{status: 404}, 404, "unknown mock url: " + conf.url]);
                    }
                });
        }
    },
    ajax_stub_restore: function () {
        if (Environment._stub) {
            Environment._stub.restore();
        }
    },
    _load_script: function (script) {
        var r = require(Environment._abs_path(script));
        $.each(r, function(k, v) { global[k] = v;});
    },
    _read_template: function (template_file) {
        var template_path = Environment._abs_path(template_file);
        var template = fs.readFileSync(template_path).toString()
            .replace(/{\%[ ]*(end)?verbatim[ ]*\%}/g, '');

        while (true) {
            // pull in server-side includes
            var m = template.match(/{\%[ ]*include[ ]+["]?([^ \%"]+)["]?[ ]*\%}/);
            if (m) {
                var text = Environment._read_template('myuw/templates/' + m[1]);
                template = template.replace(m[0], text);
            } else {
                break;
            }
        }
        return template;
    },
    _load_template: function(template_file) {
        var template = Environment._read_template(template_file);
        $('body').append(template);
    }
};

describe("Global Test Environment", function () {
    it("loads nested server-side templates", function (){
        var f = 'myuw/templates/handlebars/card/instructor_schedule/course_resource_panel.html';
        var t = Environment._read_template(f);

        assert(t.indexOf('instructor_course_resource_panel') > 0, 'template id');
        assert(t.indexOf('endtplhandlebars') < 0, 'end handlebars block stripped');
        assert(t.indexOf('verbatim') < 0, 'verbatim stripped');
        assert(t.indexOf('endverbatim') < 0, 'endverbatim stripped');
        assert(t.indexOf('show_course_textbook') < 0, 'first inclusion');
        assert(t.indexOf('list_admin_url') < 0, 'second inclusion');
        assert.equal(true, true);
    });
});


/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.Environment = Environment;
