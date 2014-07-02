var RegStatusCard = {
    render: function (reg_notices) {
        
        var source = $("#reg_status_card").html();
        var template = Handlebars.compile(source);
        
        // show registration resources
        $('body').on('click', '#show_reg_resources', function (ev) {
            
            ev.preventDefault();
            
            $("#reg_resources").toggleClass("slide-show");
            
            if ($("#reg_resources").hasClass("slide-show")) {
               $("#show_reg_resources").text("Show less...")
               $("#reg_resources").attr('aria-hidden', 'false');
            }   
            else {
               $("#show_reg_resources").text("Show more...");
               $("#reg_resources").attr('aria-hidden', 'true');
            }
                        
        });
        
        // show hold details
        $('body').on('click', '#show_reg_holds', function (ev) {
            
            ev.preventDefault();
            
            $("#reg_holds").toggleClass("slide-show");
            
            if ($("#reg_holds").hasClass("slide-show")) {
               $("#show_reg_holds").text("Hide details")
               $("#reg_holds").attr('aria-hidden', 'false');
            }
            else {
               $("#show_reg_holds").text("Show details");
               $("#reg_holds").attr('aria-hidden', 'true');
            }
            
        });

        return template({"reg_notices": reg_notices});
    },
};

    
