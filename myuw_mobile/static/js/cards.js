var Cards = {
    load_cards_in_order: function (cards, target, term){
        var loading_html = CardLoading.render();
        //Creates target divs and inserts loading messages
        $.each(cards, function (idx, card){
            var div = $("<div>", {id: card.name,
                                  html: loading_html});
            target.append(div);
        });
        //Initialize card loading/rendering
        $.each(cards, function (idx, card){
            var target = $("#" + card.name);
            Cards.load_card({'card': card,
                             'destination': target,
                             'term': term !== undefined ? term : 'current'});
        });
    },
    load_card: function (attrs) {
        if (!attrs.hasOwnProperty('card')) {
            throw "Missing card class";
        }
        if (!attrs.hasOwnProperty('destination')) {
            throw "Missing DOM destination";
        }
        var card = attrs.card;
        card.dom_target = attrs.destination;
        card.term = attrs.term;
        card.render_init();
    }
};
