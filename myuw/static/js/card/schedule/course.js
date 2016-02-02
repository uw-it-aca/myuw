var ACourseCard = {
    
    render: function (term, c_section) {
        var source = $("#a_course_card_content").html();
        var template = Handlebars.compile(source);
        var raw = template(c_section);
        $('#course_card' + c_section.index).html(raw);
    }
};
