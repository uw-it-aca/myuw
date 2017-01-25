var RenderLandingPage = function () {
    Landing.render(null, null);
    $("#landing").addClass("active");
    document.title = window.page_titles.landing;

    // Reset all the multiple resourse card render records
    resetCardRenderCalled();

    $("#landing").removeClass("active");
    $("#nav_course_list").removeClass("active");
    $("#nav_visual_schedule").removeClass("active");
    $("#nav_finabala").removeClass("active");
};
