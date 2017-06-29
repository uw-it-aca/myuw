var Global = require("./global.js");

describe("AccountsPage", function() {
    before(function () {
        Global.Environment.init({
                                    scripts: [
                                        "myuw/static/js/accounts.js",
                                        "myuw/static/js/card/tuition.js",
                                        "myuw/static/js/card/accounts/account_card.js",
                                        "myuw/static/js/card/accounts/account_medicine.js",
                                        "myuw/static/js/card/accounts/hr_payroll_card.js",
                                        "myuw/static/js/card/hfs.js",
                                        "myuw/static/js/card/library.js",
                                        "myuw/static/js/card/upass.js"
                                    ]
                                });
    });
    beforeEach(function (){
        window.user.student = false;
        window.user.employee = false;
    });
    describe('_get_card_order_by_affiliation', function() {
        it('should handle single affiliation', function() {
            var student_order = [
                TuitionCard,
                MedicineAccountsCard,
                HfsCard,
                LibraryCard,
                UPassCard,
                AccountsCard
            ];
            var employee_order = [
                MedicineAccountsCard,
                LibraryCard,
                UPassCard,
                HfsCard,
                AccountsCard
            ];
            window.user.student = true;
            var card_order = AccountsPage._get_card_order_by_affiliation();
            assert.deepEqual(card_order, student_order)

            window.user.student = false;
            window.user.employee = true;
            var card_order = AccountsPage._get_card_order_by_affiliation();
            assert.deepEqual(card_order, employee_order)
        });

        it('should default to student', function() {
            var student_order = [
                TuitionCard,
                MedicineAccountsCard,
                HfsCard,
                LibraryCard,
                UPassCard,
                AccountsCard
            ];
            var employee_order = [
                MedicineAccountsCard,
                HRPayrollCard,
                LibraryCard,
                UPassCard,
                HfsCard,
                AccountsCard
            ];
            window.user.student = true;
            window.user.employee = true;
            var card_order = AccountsPage._get_card_order_by_affiliation();
            assert.deepEqual(card_order, student_order)
        });
        it('should handle no affiliation', function() {
            var card_order = AccountsPage._get_card_order_by_affiliation();
            assert.equal(card_order, undefined)
        });
    });
    describe('order_card_list', function() {
        it('should sort cards', function() {
            var cards = '<div id="accounts_content_cards"><div data-order="0">card0</div><div data-order="1">card1</div><div data-order="2">card2</div></div><div id="accounts_sidebar_cards"></div>';
            $('body').append($(cards));
            assert.equal($("#accounts_content_cards").children().length, 3);

            AccountsPage.order_card_list(true);
            assert.equal($("#accounts_content_cards").children().length, 2);
            assert.equal($("#accounts_sidebar_cards").children().length, 1);

            AccountsPage.order_card_list(false);
            assert.equal($("#accounts_content_cards").children().length, 3);
        });

    });
});

