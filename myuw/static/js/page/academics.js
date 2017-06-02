var RenderPage = function () {
    $("#academics").removeClass("active");
    $("#app_navigation").show();
    Academics.render(null, null);
    $("#academics").addClass("active");
};
