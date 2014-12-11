//Overriding WSData.notice_data to return mocked data
var WSData = {
    notice_data: function (){
        var notices = [{"category": "Holds", "location_tags": ["notices_holds", "reg_card_holds"], "is_read": true, "is_critical": true, "notice_content": "You are not eligible to register until you check in with International Student Services, UW-Bothell, Husky Hall 1212.", "id_hash": "12930627323622ef30aa7ef9f1e0fd93", "attributes": [{"value": "Seattle", "name": "Campus", "data_type": "string"}, {"value": "today", "name": "Date", "data_type": "date"}]}, {"category": "Uncategorized", "location_tags": null, "is_read": false, "is_critical": false, "notice_content": "Summer quarter begins <b>June 23, 2014</b>", "id_hash": "771b54c35c4509bbcd1830d90a28f1a6", "attributes": [{"value": "future", "name": "Date", "data_type": "date"}, {"value": "2014-07-03", "name": "Begin", "data_type": "date"}, {"value": "2014-07-17", "name": "End", "data_type": "date"}, {"value": "Summer", "name": "Quarter", "data_type": "string"}, {"value": "http://www.uw.edu", "name": "Link", "data_type": "url"}]}, {"category": "Registration", "location_tags": ["est_reg_date", "notices_date_sort"], "is_read": false, "is_critical": true, "notice_content": "Your estimated <a href='http://www.washington.edu/students/reg/2014cal.html#Q3'>Period I Priority Registration Date</a> for fall quarter is <b>May 13, 2014</b>. Registration begins at <b>6:00 a.m.</b>", "id_hash": "8c4dcb73d9c0f3a00c4bbb160cf85e13", "attributes": [{"value": "next_week", "name": "Date", "data_type": "date"}]}, {"category": "Registration", "location_tags": ["reg_card_messages"], "is_read": false, "is_critical": true, "notice_content": "<b>Before You Register</b><br/>Beginning one week prior to each quarter's registration period you can take care of all the required Notices and Insurance&#47Optional Charges selections so that when your priority registratrion period begins, you can go directly into Web Registration. If you have not already done so, go to the <a href='https://sdb.admin.washington.edu/students/uwnetid/op_charges.asp'>Insurance&#47Optional Charges</a> services now to take care of these requirements prior to registering for summer quarter.", "id_hash": "90682cd7d80c1df339a12a44424b8971", "attributes": [{"value": "today", "name": "Date", "data_type": "date"}, {"value": "2014-06-11", "name": "Begin", "data_type": "date"}, {"value": "2014-06-14", "name": "End", "data_type": "date"}, {"value": "Summer", "name": "Quarter", "data_type": "string"}]}, {"category": "Registration", "location_tags": ["reg_card_messages"], "is_read": false, "is_critical": true, "notice_content": "<b>Before You Register MK II</b><br/>Beginning one week prior to each quarter's registration period you can take care of all the required Notices and Insurance&#47Optional Charges selections so that when your priority registratrion period begins, you can go directly into Web Registration. If you have not already done so, go to the <a href='https://sdb.admin.washington.edu/students/uwnetid/op_charges.asp'>Insurance&#47Optional Charges</a> services now to take care of these requirements prior to registering for summer quarter.", "id_hash": "9af063c86e2a8eb43a6c169767cccbb4", "attributes": [{"value": "week", "name": "Date", "data_type": "date"}]}, {"category": "Holds", "location_tags": ["notices_holds", "reg_card_holds"], "is_read": false, "is_critical": true, "notice_content": "Online ISS information session required before registration<br/>All new international students are required to complete the <a href='https://catalysttools.washington.edu/webq/survey/torre/79003'>International Student Services(ISS) Online Information Session</a> before registering for classes. You will need your UW NetID and password to access the online ISS information session. After you arrive on campus the International Student Services(ISS) must collect copies of your immigration documents.", "id_hash": "e05752938892dfd1066ed46f149ca3e7", "attributes": []}, {"category": "Holds", "location_tags": ["notices_holds", "reg_card_holds"], "is_read": false, "is_critical": true, "notice_content": "The following offices have placed <a href='http://www.washington.edu/students/reg/regrest.html#Q2'>administrative holds</a> on your academic record which will prevent further registration and/or ordering official transcripts: <br/><b>Type:</b> Registration/Transcript <b>Office:</b> Library Account Services, Suzzallo, 1st Floor 206-543-1174 <br/><b>Type:</b> Registration/Transcript <b>Office:</b> Student Fiscal Services, 129 Schmitz, 206-543-4694 <br/><b>Type:</b> Registration  <b>Office:</b> Financial Aid Office, 105 Schmitz Hall, 206-543-6101", "id_hash": "e781b938258ce61b3a0596a144d752a9", "attributes": []}, {"category": "Fees & Finances", "location_tags": ["tuition_balance", "finance_card"], "is_read": false, "is_critical": false, "notice_content": "<a href='https://sdb.admin.washington.edu/students/uwnetid/tuition.asp'>Tuition Account Balance</A>:  $12345.00 CR <a href='https://sdb.admin.washington.edu/students/uwnetid/tuition.asp'>details</a><br/><i>UW Professional & Continuing Education fees may show in both the Tuition Account Balance and the UW Professnal & Continuing Education Account Balance</i>.", "id_hash": "058f18204b865598d3ee1517c5fddb94", "attributes": [{"value": "week", "name": "Date", "data_type": "date"}]}, {"category": "Fees & Finances", "location_tags": ["pce_tuition_dup", "finance_card"], "is_read": false, "is_critical": false, "notice_content": "<i>UW Professional & Continuing Education fees may show in both the Tuition Account Balance and the UW Professnal & Continuing Education Account Balance</i>.", "id_hash": "4f07396f808a2559e8ab662fc1841088", "attributes": [{"value": "week", "name": "Date", "data_type": "date"}]}, {"category": "Fees & Finances", "location_tags": ["tuition_due_date", "finance_card", "notice_date_sort"], "is_read": false, "is_critical": true, "notice_content": "Payment of tuition and tuition-related fees for spring quarter is due <b></b>. For details, check your <a href='https://sdb.admin.washington.edu/students/UWNetID/tuition.asp'>Tuition Statement</a>", "id_hash": "10f53366ff9094adce2920bffa4e47d2", "attributes": [{"value": "next_week", "name": "Date", "data_type": "date"}]}, {"category": "Fees & Finances", "location_tags": null, "is_read": false, "is_critical": false, "notice_content": "Thank you for confirming your intention to enroll at the University of Washington for autumn quarter 2014. Your new Student Enrollment and Orientation Fee has been accepted and recorded.", "id_hash": "521e06f1ba12ef24edc663b6a8f9e5ba", "attributes": []}, {"category": "Fees & Finances", "location_tags": null, "is_read": false, "is_critical": false, "notice_content": "The Office of the Registrar has received payment for the following fees: New Student Enrollment & Orientation Fee", "id_hash": "ff34b82664bf8babcfb07ca99fa58614", "attributes": []}, {"category": "Fees & Finances", "location_tags": ["finance_card_finaid"], "is_read": false, "is_critical": false, "notice_content": "You can <a href=\"https://sdb.admin.washington.edu/students/uwnetid/finaidstatus.asp\">review the status</a> of your financial aid application online.", "id_hash": "bf730b0ea8b7152730a0fe65c0b8a7c8", "attributes": []}, {"category": "Uncategorized", "location_tags": null, "is_read": false, "is_critical": false, "notice_content": "Spring quarter ends <b>June 13, 2014<b>", "id_hash": "9cabe39f237728f3fe3de5c226a8b2fe", "attributes": [{"value": "future", "name": "Date", "data_type": "date"}, {"value": "2014-07-03", "name": "Begin", "data_type": "date"}, {"value": "2014-07-17", "name": "End", "data_type": "date"}]}];
        notices = WSData._set_notice_dates(notices);
        return notices;
    },
    _set_notice_dates: function (notices) {
        for (var i = 0; i < notices.length; i += 1) {
            var notice_attr = notices[i].attributes;
            for (var j = 0; j < notice_attr.length; j += 1) {
                if (notice_attr[j].name === "Date"){
                    var date;
                    if (notice_attr[j].value === "today") {
                        date = new Date();
                    }
                    if (notice_attr[j].value === "week") {
                        date = new Date();
                        date.setDate(date.getDate() + 1);
                    }
                    if (notice_attr[j].value === "next_week") {
                        date = new Date();
                        date.setDate(date.getDate() + 7);
                    }
                    if (notice_attr[j].value === "future") {
                        date = new Date();
                        date.setDate(date.getDate() + 14);

                    }
                    date = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();
                    notice_attr[j].value = date;
                }
            }

        }
        return notices;
    }
};


test( "get_notices_for_category", function() {
    holds_notices = Notices.get_notices_for_category("Holds");
    equal ( holds_notices.critical_count, "3", "Passed!" );
    equal ( holds_notices.unread_count, "2", "Passed!" );
    equal ( holds_notices.notices.length, "3", "Passed!" );
});

test ("get_notices_for_tag", function() {
    tag_notices = Notices.get_notices_for_tag("reg_card_messages");
    equal (tag_notices[0].id_hash, "90682cd7d80c1df339a12a44424b8971", "Passed!");
});

test ("get_total_unread", function() {
    unread_count = Notices.get_total_unread();
    equal (unread_count, "13", "Passed!");
});


test ("get_unread_count_by_category", function() {
    unread_count = Notices.get_unread_count_by_category("reg_card_messages");
    equal (unread_count.Registration, "3", "Passed!");
    equal (unread_count["Fees & Finances"], "6", "Passed!");
});

test ("get_critical_this_week", function() {
    console.log('test');
    critical_count = Notices.get_critical_this_week();
    equal (critical_count, "3", "Passed!");
});

test ("get_notices_by_date", function() {
    notices_by_date = Notices.get_notices_by_date();
    equal (notices_by_date.future.notices.length, "2", "Passed!");
    equal (notices_by_date.next_week.notices.length, "2", "Passed!");
    equal (notices_by_date.today.notices.length, "2", "Passed!");
});
