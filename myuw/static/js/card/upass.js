var UPassCard = {
    name: 'UPassCard',
    dom_target: undefined,

    render_init: function () {
        UPassCard.dom_target = $('#UPassCard');
        WSData.fetch_upass_data(UPassCard.render_upon_data, UPassCard.render_error);
    },

    render_error: function (status) {
        if (status === 543) {
            var raw = CardWithError.render("U-Pass Membership");
            UPassCard.dom_target.html(raw);
            return;
        }
        UPassCard.dom_target.hide();
    },

    render_upon_data: function () {
        UPassCard._render();
    },

    _render: function () {
        var template_data = WSData.upass_data();
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
