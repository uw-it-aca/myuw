var Instructor = {
    show_instructor: function(regid) {
        WSData.fetch_instructor_data(Instructor.render_instructor, [regid]);
    },
    
    render_instructor: function(regid) {
        var instructor_data = WSData.instructor_data();
        
        var source = $("#header").html();
        var template = Handlebars.compile(source);
        $("#page-header").html(template(
            {   DisplayName: instructor_data.DisplayName, 
                Title1: instructor_data.PersonAffiliations.EmployeePersonAffiliation.EmployeeWhitePages.Title1,
                Title2: instructor_data.PersonAffiliations.EmployeePersonAffiliation.EmployeeWhitePages.Title2,
            }
        ));

        var data = instructor_data.PersonAffiliations.EmployeePersonAffiliation.EmployeeWhitePages;
        data = $.extend(data, {Mailstop: instructor_data.PersonAffiliations.EmployeePersonAffiliation.MailStop});
        
        source = $("#instructor").html();
        template = Handlebars.compile(source);
        $("#courselist").html(template(data));

    },
};
