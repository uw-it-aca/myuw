var RenderPage = function () {
    if (myuwFeatureEnabled('instructor_schedule')) {
        $("#app_navigation").show();
    }
    CommonLoading.render_init();
};
