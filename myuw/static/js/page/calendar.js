var RenderPage = function () {
    $("#calendar").removeClass("active");
    $("#app_navigation").show();
    Calendar.render(null, null);
    $("#calendar").addClass("active");
};
