var PceBanner = {
    dom_target: undefined,

    render_init: function(dom_taget) {
        PceBanner.dom_target  = dom_taget;
        PceBanner._render();
    },

    _render: function () {
        if (user.pce) {
            var source = $("#pce_banner").html();
            var template = Handlebars.compile(source);
            PceBanner.dom_target.html(template());
            LogUtils.cardLoaded(PceBanner.name, PceBanner.dom_target);
        }
        else {
            PceBanner.dom_target.hide();
        }
    }
};
