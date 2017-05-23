var UPassCard = {
    name: 'UPassCard',
    dom_target: undefined,

    render_init: function () {
        UPassCard.dom_target = $('#UPassCard');
        WebServiceData.require({upass_data: new UPassData()}, UPassCard.render);
    },

    render_error: function (upass_resource_error) {
        if (upass_resource_error) {
            if (upass_resource_error.status === 543) {
                var raw = CardWithError.render("U-Pass Membership");
                UPassCard.dom_target.html(raw);
            } else {
                UPassCard.dom_target.hide();
            }

            return true;
        }

        return false;
    },

    render: function (resources) {
        var upass_resource = resources.upass_data;

        if (UPassCard.render_error(upass_resource.error)) {
            return;
        }

        var template_data = upass_resource.data;
        template_data.is_tacoma_student = window.user.tacoma_affil;
        template_data.is_bothell_student = window.user.bothell_affil;
        template_data.is_seattle_student = window.user.seattle_affil;
        template_data.is_pce_student = window.user.pce;
        template_data.is_pce_or_seattle_student = template_data.is_seattle_student || template_data.is_pce_student;
        var source = $("#upass_card").html();
        var template = Handlebars.compile(source);
        var raw = template(template_data);
        UPassCard.dom_target.html(raw);
        LogUtils.cardLoaded(UPassCard.name, UPassCard.dom_target);
    }
};
