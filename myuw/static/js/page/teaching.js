var RenderPage = function () {
    $("#teaching").removeClass("active");
    $("#app_navigation").show();
    Teaching.render(null, null);
    $("#teaching").addClass("active");
};
