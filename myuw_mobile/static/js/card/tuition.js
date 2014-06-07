var TuitionCard = {
    render: function (tuition_data) {
        var source = $("#tuition_card").html();
        var template = Handlebarscn s.compile(source);
        return template(tuition_data);
    },

};
