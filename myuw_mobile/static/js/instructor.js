var Instructor = {
    show_instructor: function(term, regid) {
        showLoading();
        WSData.fetch_instructor_data(Instructor.render_instructor, [term, regid]);
    },
    
    render_instructor: function(term, regid) {
        $('html,body').animate({scrollTop: 0}, 'fast');        
        var instructor_data = WSData.instructor_data(regid);
        
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


        $(".contact_instructor").on("click", function(ev) {
            var contact_info = ev.currentTarget.getAttribute("href");
            contact_info = contact_info.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("instructor_contact_"+contact_info, term);
        });

        Modal.hide();
    },
};
