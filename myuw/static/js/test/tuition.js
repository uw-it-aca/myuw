TuitionCard = require("../card/tuition.js").TuitionCard;

var assert = require("assert");
describe('Tuition', function(){
    describe('credit v debit', function(){
        it('should be a debit, not credit', function(){
            var data = TuitionCard.process_tuition("100.00")
            assert.equal(data.tuition, "100.00");
            assert.equal(data.is_credit, false);
        });
        it('should be a credit', function(){
            var data = TuitionCard.process_tuition("200.00 CR")
            assert.equal(data.tuition, "200.00");
            assert.equal(data.is_credit, true);
        });

    });
});
