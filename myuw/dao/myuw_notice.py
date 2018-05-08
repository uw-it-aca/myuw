from myuw.dao.affiliation import get_all_affiliations
from myuw.models.myuw_notice import MyuwNotice
from myuw.dao.term import get_comparison_datetime


def get_myuw_notices_for_user(request):
    date = get_comparison_datetime(request)
    active_notices = MyuwNotice.objects.filter(start__lte=date, end__gte=date)
    affiliations = get_all_affiliations(request)

    campus_notices = []
    for notice in active_notices:
        # If campus is not set show to all campuses
        if not(notice.is_bothell or notice.is_seattle or notice.is_tacoma):
            campus_notices.append(notice)
            pass
        if notice.is_seattle and affiliations['official_seattle']:
            campus_notices.append(notice)
            pass
        if notice.is_tacoma and affiliations['official_tacoma']:
            campus_notices.append(notice)
            pass
        if notice.is_bothell and affiliations['official_bothell']:
            campus_notices.append(notice)
            pass

    user_notices = []
    for notice in campus_notices:
        # If affiliation not set show to all affiliations
        if not(notice.is_alumni or notice.is_applicant or notice.is_grad or
                notice.is_grad_c2 or notice.is_pce or notice.is_student or
                notice.is_undergrad or notice.is_undergrad_c2 or
                notice.is_fyp or notice.is_past_student or
                notice.is_clinician or notice.is_employee or
                notice.is_faculty or notice.is_instructor or
                notice.is_past_employee or notice.is_retiree or
                notice.is_staff_employee or notice.is_stud_employee):
            user_notices.append(notice)
        if notice.is_alumni and affiliations["alumni"]:
            user_notices.append(notice)
            pass
        if notice.is_applicant and affiliations["applicant"]:
            user_notices.append(notice)
            pass
        if notice.is_grad and affiliations["grad"]:
            user_notices.append(notice)
            pass
        if notice.is_grad_c2 and affiliations["grad_c2"]:
            user_notices.append(notice)
            pass
        if notice.is_pce and affiliations["pce"]:
            user_notices.append(notice)
            pass
        if notice.is_student and affiliations["student"]:
            user_notices.append(notice)
            pass
        if notice.is_undergrad and affiliations["undergrad"]:
            user_notices.append(notice)
            pass
        if notice.is_undergrad_c2 and affiliations["undergrad_c2"]:
            user_notices.append(notice)
            pass
        if notice.is_fyp and affiliations["fyp"]:
            user_notices.append(notice)
            pass
        if notice.is_past_student and affiliations["past_stud"]:
            user_notices.append(notice)
            pass
        if notice.is_clinician and affiliations["clinician"]:
            user_notices.append(notice)
            pass
        if notice.is_employee and affiliations["employee"]:
            user_notices.append(notice)
            pass
        if notice.is_faculty and affiliations["faculty"]:
            user_notices.append(notice)
            pass
        if notice.is_instructor and affiliations["instructor"]:
            user_notices.append(notice)
            pass
        if notice.is_past_employee and affiliations["past_employee"]:
            user_notices.append(notice)
            pass
        if notice.is_retiree and affiliations["retiree"]:
            user_notices.append(notice)
            pass
        if notice.is_staff_employee and affiliations["staff_employee"]:
            user_notices.append(notice)
            pass
        if notice.is_stud_employee and affiliations["stud_employee"]:
            user_notices.append(notice)
            pass

    return user_notices
