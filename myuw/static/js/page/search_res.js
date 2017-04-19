var RenderPage = function () {
    if (myuwFeatureEnabled('instructor_schedule')) {
        $("#app_navigation").show();
    }
    CommonLoading.render_init();

    // set search term in input field
    var input = $("#search-results-page"),
        search_term = getUrlParameter("q");
    $(input).val(search_term);

};
