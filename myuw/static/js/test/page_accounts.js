var Global = require("./global.js");

describe("AccountsPage", function() {
    before(function () {
        Global.Environment.init({
            scripts: [
                "myuw/static/js/accounts.js",
                "myuw/static/js/cards.js",
                "myuw/static/js/card/loading.js",
                "myuw/static/js/card/accounts/tuition.js",
                "myuw/static/js/card/accounts/uwnetid.js",
                "myuw/static/js/card/accounts/account_medicine.js",
                "myuw/static/js/card/accounts/hr_payroll_card.js",
                "myuw/static/js/card/accounts/hfs_sea.js",
                "myuw/static/js/card/accounts/husky.js",
                "myuw/static/js/card/accounts/library.js",
                "myuw/static/js/card/accounts/upass.js"
            ]
        });
    });
    beforeEach(function (){
        window.page = "accounts";
        window.user.employee = false;
        window.user.instructor = false;
        window.user.student = false;
        window.user.seattle = false;
        window.user.stud_employee = false;
        window.user.past_stud = false;
        window.user.past_employee = false;
        window.user.retiree = false;
    });
    describe('_get_card_order_by_affiliation', function() {

        it('should handle clinician affiliation', function() {
            var order = [
                MedicineAccountsCard,
                HuskyCard,
                LibraryCard,
                UPassCard,
                UwnetidCard
            ];
            window.user.employee = true;  // including clinician
            var card_order = AccountsPage._get_card_order_by_affiliation();
            assert.deepEqual(card_order, order)
        });

        it('should handle student affiliation', function() {
            var student_order = [
                TuitionCard,
                MedicineAccountsCard,
                HuskyCard,
                LibraryCard,
                UPassCard,
                UwnetidCard
            ];
            window.user.student = true;
            var card_order = AccountsPage._get_card_order_by_affiliation();
            assert.deepEqual(card_order, student_order)
        });

        it('should handle past student affiliation', function() {
            var student_order = [
                MedicineAccountsCard,
                HuskyCard,
                LibraryCard,
                UwnetidCard
            ];
            window.user.past_stud = true;
            var card_order = AccountsPage._get_card_order_by_affiliation();
            assert.deepEqual(card_order, student_order)
        });

        it('should handle seattle student affiliation', function() {
            var student_order = [
                TuitionCard,
                MedicineAccountsCard,
                HuskyCard,
                HfsSeaCard,
                LibraryCard,
                UPassCard,
                UwnetidCard
            ];
            window.user.student = true
            window.user.undergrad = true;
            window.user.seattle = true;
            var card_order = AccountsPage._get_card_order_by_affiliation();
            assert.deepEqual(card_order, student_order)
        });

        it('should handle student employee affiliation', function() {
            var stud_employee_order = [
                TuitionCard,
                MedicineAccountsCard,
                HuskyCard,
                HRPayrollCard,
                LibraryCard,
                UPassCard,
                UwnetidCard
            ];
            window.user.student = true;
            window.user.stud_employee = true;
            var card_order = AccountsPage._get_card_order_by_affiliation();
            assert.deepEqual(card_order, stud_employee_order)
        });

        it('should handle employee affiliation', function() {
            var employee_order = [
                MedicineAccountsCard,
                HuskyCard,
                LibraryCard,
                UPassCard,
                UwnetidCard
            ];
            window.user.employee = true;
            var card_order = AccountsPage._get_card_order_by_affiliation();
            assert.deepEqual(card_order, employee_order)
        });

        it('should handle past employee affiliation', function() {
            var employee_order = [
                MedicineAccountsCard,
                HuskyCard,
                LibraryCard,
                UwnetidCard
            ];
            window.user.past_employee = true;
            var card_order = AccountsPage._get_card_order_by_affiliation();
            assert.deepEqual(card_order, employee_order)
        });

        it('should handle instructor affiliation', function() {
            var instructor_order = [
                MedicineAccountsCard,
                HuskyCard,
                HRPayrollCard,
                LibraryCard,
                UPassCard,
                UwnetidCard
            ];
            window.user.instructor = true;
            window.user.employee = true;
            var card_order = AccountsPage._get_card_order_by_affiliation();
            assert.deepEqual(card_order, instructor_order)
        });

        it('should handle no affiliation', function() {
            var default_order = [
                MedicineAccountsCard,
                LibraryCard,
                UwnetidCard
            ];
            var card_order = AccountsPage._get_card_order_by_affiliation();
            assert.deepEqual(card_order, default_order)
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
