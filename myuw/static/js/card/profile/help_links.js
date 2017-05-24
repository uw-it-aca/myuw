var ProfileHelpLinksCard = {
    name: 'HelpLinksCard',
    dom_target: undefined,

    render_init: function() {
        ProfileHelpLinksCard.render();
    },

    render: function() {
        var source   = $("#profile_help_links_card").html();
        var template = Handlebars.compile(source);
        var compiled = template({
            is_student: (window.user.student || window.user.stud_employee),
            is_employee: (window.user.employee || window.user.stud_employee)
        });
        ProfileHelpLinksCard.dom_target.html(compiled);
    }
};


/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.ProfileHelpLinksCard = ProfileHelpLinksCard;
