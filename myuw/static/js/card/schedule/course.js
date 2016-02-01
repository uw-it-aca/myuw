var ACourseCard = {
    
    render: function (term, c_section) {
        var source = $("#a_course_card_content").html();
        var template = Handlebars.compile(source);
        $('#course_card' + c_section.index).html(template(c_section));
    }
};
