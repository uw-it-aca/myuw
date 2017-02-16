var RenderPage = function() {
    $("#teaching").removeClass("active");
    $("#app_navigation").show();
    PhotoClassList.render();
    $("#teaching").addClass("active");
};
