var CourseCard = {
    name: 'CourseCard',
    dom_target: undefined,
    term: 'current',

    render_init: function() {
        WSData.fetch_course_data_for_term(CourseCard.term, CourseCard.render_upon_data);
    },

    render_upon_data: function() {
        if (!CourseCard._has_all_data()) {
            CourseCard.dom_target.html(CardWithError.render());
            return;
        }
        CourseCard._render();
    },

    _has_all_data: function () {
        if (WSData.normalized_course_data()) {
            return true;
        }
        return false;
    },

    _render: function () {
        var term = CourseCard.term;
        var course_data = WSData.normalized_course_data(term);
        if (course_data.sections.length == 0) {
            CourseCard.dom_target.html(CardWithNoCourse.render(term));
            return;
        }

        var index;
        for (index = 0; index < course_data.sections.length; index += 1) {
            course_data.sections[index].index = index;
            if (course_data.sections[index].class_website_url || course_data.sections[index].canvas_url) {
                course_data.sections[index].has_resources = true;
            }
        }
        var source = $("#course_card_content").html();
        var courses_template = Handlebars.compile(source);

        $("body").on('shown.bs.collapse', function (event) {
                $(event.target).parent().find("div.accordion-footer > a > span.show_more").hide();
                $(event.target).parent().find("div.accordion-footer > a > span.show_less").show();
                $(event.target).attr('aria-hidden', false);
            });
        $("body").on('hidden.bs.collapse', function (event) {
                $(event.target).parent().find("div.accordion-footer > a > span.show_more").show();
                $(event.target).parent().find("div.accordion-footer > a > span.show_less").hide();
                $(event.target).attr('aria-hidden', true);
            });

        CourseCard.dom_target.html(courses_template(course_data));
        CourseCard.add_events(term);
    },

    add_events: function(term) {
        $('.canvasGradeBox').popover({content: gettext('canvas_grade_tip'),
                                      selector: '.canvasGradeLabel',
                                      placement: 'bottom'});

        $(".course_website").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_website_"+course_id, term);
        });

        $(".course_canvas_site").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_canvas_website_"+course_id, term);
        });

        $(".show_map").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            var building = ev.currentTarget.getAttribute("rel");
            building = building.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("show_map_from_course_list_"+building, term);
        });
        
        
        $(".slide-link").on("click", function(ev) {
            ev.preventDefault();
            var hidden_block = $(ev.target).parent().siblings(".slide-hide")[0];
            var slide_link = this;
                        
            $(hidden_block).toggleClass("slide-show");

            if ($(hidden_block).hasClass("slide-show")) {
                $(slide_link).text("Show less")
                $(slide_link).attr('title', 'Show less course information');
                $(hidden_block).attr('aria-hidden', 'false');
                //WSData.log_interaction("show_final_card", term);
            }
            else {
                
                $(slide_link).attr('title', 'Show more course information');
                $(hidden_block).attr('aria-hidden', 'true');
                
                setTimeout(function() {
                      $(slide_link).text("Show more");
                }, 700);
 
            }
        });


        $(".instructor").on("click", function(ev) {
            WSData.log_interaction("view_instructor_from_course_list", term);
            var hist = window.History;
            if (term) {
                hist.pushState({
                    state: "instructor",
                    instructor: ev.target.rel,
                    term: term
                },  "", "/mobile/instructor/"+term+"/"+ev.target.rel);
            }
            else {
                hist.pushState({
                    state: "instructor",
                    instructor: ev.target.rel
                },  "", "/mobile/instructor/"+ev.target.rel);
            }
            return false;
        });
    },
};
