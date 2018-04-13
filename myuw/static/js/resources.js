var Resources = {

    render: function() {
        showLoading();
        Resources.load_resource_data();
    },

    make_html: function () {
        if (WSData.resource_data()) {
            Handlebars.registerPartial('resource_content', $("#resource_content").html());
            var resource_data = WSData.resource_data();
            $('html,body').animate({scrollTop: 0}, 'fast');
            var source = $("#resource_page").html();
            var template = Handlebars.compile(source);
            var content = template({'categories': resource_data});
            $("#main-content").html(content);
            Resources.init_events();
        }

    },

    load_resource_data: function () {
        WSData.fetch_resource_data(Resources.make_html,
            Resources.resource_error);

    },

    resource_error: function () {
        return;
    },

    init_events: function () {
        if(window.location.hash){
            setTimeout(function(){
                $('html, body').animate({
                    scrollTop: $(window.location.hash).offset().top
                }, 'fast');
            }, 500);
        }

        $(".category-pin, .category-unpin").click(function(ev){
            var cat_id = $(ev.target).val(),
                pin = true;
            if ($(ev.target).attr('class').indexOf('unpin') > -1){
                pin = false;
                $(ev.target).addClass('hidden');
                $(ev.target).siblings('.category-pin').removeClass('hidden');
            } else {
                $(ev.target).addClass('hidden');
                $(ev.target).siblings('.category-unpin').removeClass('hidden');
            }

            Resources.handle_pin_click(cat_id, pin);
        });

        $("#scroll-to-top").click(function(ev){
            $('html,body').animate({scrollTop: 0}, 'fast');
        });
    },

    handle_pin_click: function (category_id, pin) {
        WSData.handle_resource_pin(Resources.pinned_success,
                                   Resources.resource_error,
                                   undefined,
                                   category_id,
                                   pin);
    },

    pinned_success: function () {
        return;
    }



};
