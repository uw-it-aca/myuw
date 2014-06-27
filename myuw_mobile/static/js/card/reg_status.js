var RegStatusCard = {
    render: function (reg_notices) {
        
        var source = $("#reg_status_card").html();
        var template = Handlebars.compile(source);
        
        // show registration resources
        $('body').on('click', '#reg_show_resources', function (ev) {
            
            ev.preventDefault();
            
            $("#reg_resources").toggleClass("slide-show");
            
            if ($("#reg_show_resources").text() == "Show more...")
               $("#reg_show_resources").text("Show less...")
            else
               $("#reg_show_resources").text("Show more...");
        });
        
        // show hold details
        $('body').on('click', '#reg_show_holds', function (ev) {
            
            ev.preventDefault();
            
            $("#reg_holds").toggleClass("slide-show");
            
            if ($("#reg_show_holds").text() == "Show details")
               $("#reg_show_holds").text("Hide details")
            else
               $("#reg_show_holds").text("Show details");
            
        });

        return template({"reg_notices": reg_notices});
    },
};

    
