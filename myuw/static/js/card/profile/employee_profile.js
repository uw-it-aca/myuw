var EmployeeInfoCard = {
    name: 'EmployeeInfoCard',
    dom_target: undefined,

    hide_card: function() {
        if (window.user.employee || window.user.stud_employee) {
            return false;
        }
        return true;
    },

    render_init: function() {
        if (EmployeeInfoCard.hide_card()) {
            $("#EmployeeInfoCard").hide();
            return;
        }
        WSData.fetch_directory_data(EmployeeInfoCard.render_upon_data,
                                    EmployeeInfoCard.render_error);
    },

    render_upon_data: function () {
        if (WSData.directory_data()) {
            EmployeeInfoCard._render();
        }
    },

    _render: function () {
        var emp_white_page = WSData.directory_data();
        Handlebars.registerPartial('workday_link', $("#workday_link").html());
        var source = $("#emp_white_page_card").html();
        var template = Handlebars.compile(source);
        var i;
        // enhanced directory info
        emp_white_page.is_tacoma = window.user.tacoma;

        if (emp_white_page.positions.length > 0) {
            for (i = 0; i < emp_white_page.positions.length; i++) {
                if (emp_white_page.positions[i].is_primary ) {
                    emp_white_page.position1 = emp_white_page.positions[i];
                    break;
                }
            }
        }

        if (emp_white_page.email_addresses.length > 0) {
            emp_white_page.has_email = true;
            emp_white_page.email1 = emp_white_page.email_addresses[0];
        }

        if (emp_white_page.addresses.length > 0) {
            emp_white_page.address1 = emp_white_page.addresses[0];
        } else {
            emp_white_page.no_address = (emp_white_page.mailstop === null);
            // no_address and no mailstop
        }

        if (emp_white_page.faxes.length > 0) {
            emp_white_page.fax1 = emp_white_page.faxes[0];
        } else {
            emp_white_page.no_fax = true;
        }

        if (emp_white_page.phones.length > 0) {
            emp_white_page.phone1 = emp_white_page.phones[0];
        } else {
            emp_white_page.no_phone = true;
        }

        if (emp_white_page.mobiles.length > 0) {
            emp_white_page.mobile1 = emp_white_page.mobiles[0];
        } else {
            emp_white_page.no_mobile = true;
        }

        if (emp_white_page.voice_mails.length > 0) {
            emp_white_page.voice_mail1 = emp_white_page.voice_mails[0];
        } else {
            emp_white_page.no_voice_mail = true;
        }
        emp_white_page.no_pmvf = (emp_white_page.no_phone &&
                                  emp_white_page.no_mobile &&
                                  emp_white_page.no_voice_mail &&
                                  emp_white_page.no_fax);

        EmployeeInfoCard.dom_target.html(template(emp_white_page));
        LogUtils.cardLoaded(EmployeeInfoCard.name, EmployeeInfoCard.dom_target);
    },

    render_error: function () {
        $("#EmployeeInfoCard").hide();
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.EmployeeInfoCard = EmployeeInfoCard;
