var Global = require("./global.js");

describe("VisualScheduleCard", function() {
    before(function () {
        var render_id = 'test_visual_schedule';

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/visual_schedule.js",
                "myuw/static/js/card/schedule/visual.js",
                "myuw/static/js/card/schedule/final_panel.js",
                "myuw/static/js/card/schedule/sp_final.js"
            ],
            templates: [
                'myuw/templates/handlebars/visual_schedule.html',
                'myuw/templates/handlebars/card/schedule/visual.html',
                'myuw/templates/handlebars/card/schedule/visual_day.html',
                'myuw/templates/handlebars/card/schedule/final_day.html',
                'myuw/templates/handlebars/card/schedule/final_panel.html'
            ]
        });

        window.card_display_dates = {};
        VisualScheduleCard.dom_target = $('#' + render_id);
    });

    describe('card renders', function() {
        before(function (done) {
            Global.Environment.ajax_stub({
                '/api/v1/instructor_schedule/2013,spring': 'api/v1/instructor_schedule/eight.json',
                '/api/v1/schedule/2013,spring': 'api/v1/schedule/eight.json'
            });

            window.enabled_features = { 'instructor_schedule': true };

            // clear cache
            WSData._course_data = {}
            WSData._instructed_course_data = {}

            $(window).on("myuw:card_load", function () {
                done();
            });

            VisualScheduleCard.term = '2013,spring'
            VisualScheduleCard.render_init();
        });

        it('for netid eight', function () {
            var $schedule = VisualScheduleCard.dom_target.find('.visual-schedule');
            assert.equal($schedule.length, 1);
            assert.equal($schedule.find('> .six-day').length, 6);
            assert.equal($schedule.find('> .six-day').eq(0).find('.visual-course').length, 2);
            assert.equal($schedule.find('> .six-day').eq(5).find('.visual-course').length, 1);
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });

    describe('_sections_are_same', function() {
        it('should handle identical lists', function() {
            var list1 = {sections: [{course_number: "123", curriculum_abbr: "ASD"}, {course_number: "456", curriculum_abbr: "ASD"}, {course_number: "789", curriculum_abbr: "ASD"}]};
            var list2 = {sections: [{course_number: "123", curriculum_abbr: "ASD"}, {course_number: "456", curriculum_abbr: "ASD"}, {course_number: "789", curriculum_abbr: "ASD"}]};
            var are_same = VisualScheduleCard._sections_are_same(list1, list2);
            assert.equal(are_same, true)
        });

        it('should handle different sorts', function() {
            var list1 = {sections: [{course_number: "123", curriculum_abbr: "ASD"}, {course_number: "456", curriculum_abbr: "ASD"}, {course_number: "789", curriculum_abbr: "ASD"}]};
            var list2 = {sections: [{course_number: "789", curriculum_abbr: "ASD"}, {course_number: "456", curriculum_abbr: "ASD"}, {course_number: "123", curriculum_abbr: "ASD"}]};
            var are_same = VisualScheduleCard._sections_are_same(list1, list2);
            assert.equal(are_same, true)
        });

        it('should handle different lists', function() {
            var list1 = {sections: [{course_number: "123", curriculum_abbr: "ASD"}, {course_number: "456", curriculum_abbr: "ASD"}, {course_number: "789", curriculum_abbr: "ASD"}]};
            var list2 = {sections: [{course_number: "123", curriculum_abbr: "DEF"}, {course_number: "456", curriculum_abbr: "DEF"}, {course_number: "789", curriculum_abbr: "DEF"}]};
            var are_same = VisualScheduleCard._sections_are_same(list1, list2);
            assert.equal(are_same, false)
        });
        it('should handle different lengths', function() {
            var list1 = {sections: [{course_number: "123", curriculum_abbr: "ASD"}, {course_number: "456", curriculum_abbr: "ASD"}, {course_number: "789", curriculum_abbr: "ASD"}]};
            var list2 = {sections: []};
            var are_same = VisualScheduleCard._sections_are_same(list1, list2);
            assert.equal(are_same, false)
        });
    });

    describe('_get_week_range_from_date', function() {
        it('should get dates across months', function() {
            var range = VisualScheduleCard._get_week_range_from_date("2017-09-01");
            assert.equal(range[0].format("YYYY-MM-DD"), "2017-08-28");
            assert.equal(range[1].format("YYYY-MM-DD"), "2017-09-03");
        });
        it('should get dates across years', function() {
            var range = VisualScheduleCard._get_week_range_from_date("2016-01-01");
            assert.equal(range[0].format("YYYY-MM-DD"), "2015-12-28");
            assert.equal(range[1].format("YYYY-MM-DD"), "2016-01-03");
        });
    });

    describe('_get_dates_for_section', function() {
        it('should get dates for a regular class', function() {
            window.term.first_day_quarter = "2017-01-20";
            window.term.last_day_instruction = "2017-05-10";
            window.term.summer_term = ""
            var dates = VisualScheduleCard._get_dates_for_section({start_date: "None", end_date: "None"});
            assert.equal(dates[0].format("YYYY-MM-DD"), "2017-01-20");
            assert.equal(dates[1].format("YYYY-MM-DD"), "2017-05-10");
        });
        it('should get dates for an off term class', function() {
            var dates = VisualScheduleCard._get_dates_for_section({start_date: "2017-01-20", end_date: "2017-05-10"});
            assert.equal(dates[0].format("YYYY-MM-DD"), "2017-01-20");
            assert.equal(dates[1].format("YYYY-MM-DD"), "2017-05-10");
        });
        it('should handle a summer course a-term', function() {
            window.term.first_day_quarter = "2017-01-20";
            window.term.aterm_last_date = "2017-05-10";
            window.term.summer_term = "a-term";
            var dates = VisualScheduleCard._get_dates_for_section({start_date: "None", end_date: "None"});
            assert.equal(dates[0].format("YYYY-MM-DD"), "2017-01-20");
            assert.equal(dates[1].format("YYYY-MM-DD"), "2017-05-10");
        });
        it('should handle a summer course b-term', function() {
            window.term.bterm_first_date = "2017-01-20";
            window.term.last_day_instruction = "2017-05-10";
            window.term.summer_term = "b-term";
            var dates = VisualScheduleCard._get_dates_for_section({start_date: "None", end_date: "None"});
            assert.equal(dates[0].format("YYYY-MM-DD"), "2017-01-20");
            assert.equal(dates[1].format("YYYY-MM-DD"), "2017-05-10");
        });
        it('should handle a future regular quarter', function() {
            window.future_term = "2017,spring";
            window.future_term_data = {};
            window.future_term_data.first_day_quarter = "2017-01-20";
            window.future_term_data.last_day_instruction = "2017-05-10";
            var dates = VisualScheduleCard._get_dates_for_section({start_date: "None", end_date: "None", summer_term: ""});
            assert.equal(dates[0].format("YYYY-MM-DD"), "2017-01-20");
            assert.equal(dates[1].format("YYYY-MM-DD"), "2017-05-10");
        });

        it('should handle a future summer quarter', function() {
            window.future_term = "2017,summer,a-term";
            window.future_term_data = {};
            window.future_term_data.first_day_quarter = "2017-01-20";
            window.window.future_term_data.aterm_last_date = "2017-05-10";
            var dates = VisualScheduleCard._get_dates_for_section({start_date: "None", end_date: "None", summer_term: "A-term"});
            assert.equal(dates[0].format("YYYY-MM-DD"), "2017-01-20");
            assert.equal(dates[1].format("YYYY-MM-DD"), "2017-05-10");
        });
    });

    describe('_get_weeks_from_range', function() {
        it('should get weeks', function() {
            var start = moment.utc("2017-06-01");
            var end = moment.utc("2017-06-12");

            var weeks = VisualScheduleCard._get_weeks_from_range([start, end]);
            assert.deepEqual(Object.keys(weeks), ["22","23","24"]);
            assert.equal(weeks[Object.keys(weeks)[0]].start_date.format("YYYY-MM-DD"), "2017-05-29");
            assert.equal(weeks[Object.keys(weeks)[0]].end_date.format("YYYY-MM-DD"), "2017-06-04");
        });

        it('should work across years', function() {
            var start = moment.utc("2017-12-01");
            var end = moment.utc("2018-01-12");

            var weeks = VisualScheduleCard._get_weeks_from_range([start, end]);
            assert.deepEqual(Object.keys(weeks), ["48","49","50","51","52","53","54"]);

            assert.equal(weeks[Object.keys(weeks)[0]].start_date.format("YYYY-MM-DD"), "2017-11-27");
            assert.equal(weeks[Object.keys(weeks)[0]].end_date.format("YYYY-MM-DD"), "2017-12-03");
            assert.equal(weeks[Object.keys(weeks)[6]].start_date.format("YYYY-MM-DD"), "2018-01-08");
            assert.equal(weeks[Object.keys(weeks)[6]].end_date.format("YYYY-MM-DD"), "2018-01-14");
        });
    });

    describe('_get_default_period', function() {
        it('should get the default period', function() {
            window.card_display_dates.comparison_date = "2017-06-05";
            var start = moment.utc("2017-06-01");
            var end = moment.utc("2017-06-12");
            var weeks = VisualScheduleCard._get_weeks_from_range([start, end]);

            var default_period = VisualScheduleCard._get_default_period(null, weeks);
            assert.equal(default_period, "23")
        });

        it('should default to first if today is outside of the schedule range', function() {
            window.card_display_dates.comparison_date = "2017-09-05";
            var start = moment.utc("2017-06-01");
            var end = moment.utc("2017-06-12");
            var weeks = VisualScheduleCard._get_weeks_from_range([start, end]);

            var default_period = VisualScheduleCard._get_default_period(weeks, null);
            assert.equal(default_period, "22")
        });
    });

    describe('_add_sections_to_weeks', function() {
        it('should add sections to weeks', function() {
            var start = moment.utc("2017-06-01");
            var end = moment.utc("2017-06-12");

            var weeks = VisualScheduleCard._get_weeks_from_range([start, end]);
            var sections = [{start_date: "2017-06-01", end_date: "2017-06-2"}, {start_date: "2017-06-3", end_date: "2017-06-10"}, {start_date: "2017-06-12", end_date: "2017-06-13"}];
            var weeks_with_sections = VisualScheduleCard._add_sections_to_weeks(weeks, sections);
            var week_keys = Object.keys(weeks_with_sections);

            assert.equal(weeks_with_sections[week_keys[0]].sections.length, 2);
            assert.equal(weeks_with_sections[week_keys[1]].sections.length, 1);
            assert.equal(weeks_with_sections[week_keys[2]].sections.length, 1);
        });
    });

    describe('_consolidate_weeks', function() {
        it('should consolidate weeks', function() {
            var start = moment.utc("2017-06-01");
            var end = moment.utc("2017-06-12");

            var weeks = VisualScheduleCard._get_weeks_from_range([start, end]);
            var sections = [{start_date: "2017-06-01", end_date: "2017-06-10", course_number: "123", curriculum_abbr: "ASD"},
                {start_date: "2017-06-3", end_date: "2017-06-10", course_number: "456", curriculum_abbr: "ASD"},
                {start_date: "2017-06-12", end_date: "2017-06-12", course_number: "789", curriculum_abbr: "ASD"}];
            var weeks_with_sections = VisualScheduleCard._add_sections_to_weeks(weeks, sections);
            var consolidated = VisualScheduleCard._consolidate_weeks(weeks_with_sections);
            var week_keys = Object.keys(consolidated);
            assert.deepEqual(week_keys, ["23", "24"])
        });

        it('should handle a, ab, a periods', function() {
            var start = moment.utc("2017-06-12");
            var end = moment.utc("2017-07-20");

            var weeks = VisualScheduleCard._get_weeks_from_range([start, end]);
            var sections = [{start_date: "2017-06-12", end_date: "2017-07-20", course_number: "123", curriculum_abbr: "ASD"},
                {start_date: "2017-06-21", end_date: "2017-06-24", course_number: "456", curriculum_abbr: "ASD"}];
            var weeks_with_sections = VisualScheduleCard._add_sections_to_weeks(weeks, sections);
            var consolidated = VisualScheduleCard._consolidate_weeks(weeks_with_sections);
            var week_keys = Object.keys(consolidated);

            assert.equal(week_keys.length, 3)
            assert.equal(weeks[week_keys[0]].sections.length, 1)
            assert.equal(weeks[week_keys[1]].sections.length, 2)
            assert.equal(weeks[week_keys[2]].sections.length, 1)

        });
    });

    describe('_get_schedule_range', function() {
        it('should get correct range', function() {
            window.term.first_day_quarter = "2017-01-20";
            window.term.last_day_instruction = "2017-05-10";
            var sections = [{start_date: "2017-06-01", end_date: "2017-06-2"},
                {"start_date": "None"},
                {start_date: "2017-06-11", end_date: "2017-06-12"}];
            var range = VisualScheduleCard._get_schedule_range({"sections": sections});
            assert.equal(range[0].format("YYYY-MM-DD"), "2017-01-20");
            assert.equal(range[1].format("YYYY-MM-DD"), "2017-06-12")

        });
    });

    describe('_add_to_periods', function() {
        it('should add to empty periods', function() {
            var dates = ["2013-04-01", "2013-05-01"],
                section = "i'm a section";
            var periods = VisualScheduleCard._add_to_periods(dates, section, {});
            assert.equal(Object.keys(periods).length, 1);
        });
        it('should add to existing periods', function() {
            var dates = [moment("2013-04-01"), moment("2013-05-01")],
                section = "i'm a section";
            var periods = VisualScheduleCard._add_to_periods(dates, section, {});

            periods = VisualScheduleCard._add_to_periods(dates, section, periods);
            assert.equal(Object.keys(periods).length, 1);
            assert.equal(periods[0].sections.length, 2);
        });
        it('should create new period with existing', function() {
            var dates = [moment("2013-04-01"), moment("2013-05-01")],
                dates2 = [moment("2013-05-01"), moment("2013-06-01")],
                section = "i'm a section";
            var periods = VisualScheduleCard._add_to_periods(dates, section, {});

            periods = VisualScheduleCard._add_to_periods(dates2, section, periods);
            assert.equal(Object.keys(periods).length, 2);
            assert.equal(periods[0].sections.length, 1);
            assert.equal(periods[1].sections.length, 1);
        });

    });
});

