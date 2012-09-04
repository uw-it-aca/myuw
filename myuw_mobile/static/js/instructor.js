var Instructor = {
    show_instructor: function(regid) {
        WSData.fetch_course_data(Instructor.render_instructor, [regid]);
    },

    render_instructor: function(regid) {
        alert("Show instructor: "+regid);
    }
};
