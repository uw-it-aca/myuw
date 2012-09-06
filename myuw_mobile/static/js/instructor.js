var Instructor = {
    show_instructor: function(regid) {
        WSData.fetch_instructor_data(Instructor.render_instructor, [regid]);
    },
    
    render_instructor: function(regid) {
        var instructor_data = WSData.instructor_data();
        
        var source = $("#header").html();
        var template = Handlebars.compile(source);
        $("#quarter-info").html(template({DisplayName: instructor_data.DisplayName}));

        var data = instructor_data.PersonAffiliations.EmployeePersonAffiliation.EmployeeWhitePages;
        
        source = $("#instructor").html();
        template = Handlebars.compile(source);
        $("#courselist").html(template(data));

    },
        

};
