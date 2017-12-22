var SidebarLinks = {
    name: 'SidebarLinks',
    dom_target: undefined,

    render_init: function () {
        var link_category = window.sidebar_links_category;
        if (link_category !== undefined){
            WSData.fetch_category_links(SidebarLinks._render, SidebarLinks.render_error, [link_category]);
        } else {
            SidebarLinks.hide_card();
        }
    },

    render_error: function (status) {
        SidebarLinks.hide_card();
    },

    _render: function () {
        var data = WSData.category_link_data(window.sidebar_links_category),
            source = $("#sidebar_link_card").html(),
            template = Handlebars.compile(source);

        SidebarLinks.dom_target.html(template(data));
    },

    hide_card: function () {
        SidebarLinks.dom_target.hide();

    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.SidebarLinks = SidebarLinks;
