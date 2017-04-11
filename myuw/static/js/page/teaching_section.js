var RenderPage = function () {
    $("#teaching").removeClass("active");
    $("#app_navigation").show();
    TeachingSection.render(null, null);
    $("#teaching").addClass("active");
};
