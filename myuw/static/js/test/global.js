var path = require("path");
var fs = require("fs");
var sinon = require("sinon");

var Environment = {
    _stub: null,

    init: function (config) {
        if (!config) {
            config = {};
        }

        // create test document
        var window = require('jsdom').jsdom().defaultView;

        // pull in supporting tools
        var $ = require('jquery')(window);
        global.$ = $;
        global.window = window;
        global.assert = require("assert");
        global.moment = require("moment");
        global.Handlebars = require("../../vendor/js/handlebars-v2.0.0.js");
        var MomentTZ = require("moment-timezone");
        var HandlebarsHelpers = require("../handlebars-helpers.js")

        // set up client environment
        window.user = {};
        window.user.student = true;

        // default test term
        window.term = {};
        window.term.year = 2013;
        window.term.quarter = 'spring';

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
        Environment._load_script('../myuw_m.js');
        Environment._load_script('../ws_data.js');
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
    ajax_stub: function (json_data_file) {
        var json_file = path.join(__dirname, 'ajax', json_data_file);
        var json_data = JSON.parse(fs.readFileSync(json_file));
        Environment._stub = sinon.stub($, 'ajax');
        Environment._stub.yieldsTo('success', json_data);
    },
    ajax_stub_restore: function () {
        if (Environment._stub) {
            Environment._stub.restore();
        }
    },
    _load_script(script) {
        $.each(require(script), function(k, v) { global[k] = v; });
    },
    _read_template(template_file) {
        var raw = fs.readFileSync(template_file).toString();
        template = raw.replace(/{\%[ ]+load[ ]+templatetag_handlebars[ ]+\%}/, '')
            .replace(/{\%[ ]*tplhandlebars[ ]+["]?([^ \%]+)["]?[ ]*\%}/,
                     '<script id="$1" type="text/x-handlebars-template">')
            .replace(/{\%[ ]*endtplhandlebars[ ]*\%}/, 
                     '</script>');
        return template;
    },
    _load_template(template_file) {
        var template = Environment._read_template(template_file);

        while (true) {
            // pull in server-side includes
            var m = template.match(/{\%[ ]*include[ ]+["]?([^ \%"]+)["]?[ ]*\%}/);
            if (m) {
                var text = Environment._read_template('myuw/templates/' + m[1]);
                text = text.replace(/{\%[ ]*(end)?verbatim[ ]*\%}/g, '');
                template = template.replace(m[0], text);
            } else {
                break;
            }
        }

        $('body').append(template);
    }
};


/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.Environment = Environment;
