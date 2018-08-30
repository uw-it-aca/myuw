from myuw.dao.affiliation import get_all_affiliations
from myuw.models.myuw_notice import MyuwNotice
from myuw.dao.term import get_comparison_datetime_with_tz


def get_myuw_notices_for_user(request):
    date = get_comparison_datetime_with_tz(request)
    fetched_notices = MyuwNotice.objects.filter(start__lte=date)
    active_notices = []

    for notice in fetched_notices:

        if notice.end is None:
            active_notices.append(notice)
            continue
        if notice.end is not None:
            if notice.end >= date:
                active_notices.append(notice)

    affiliations = get_all_affiliations(request)

    user_notices = []
    for notice in active_notices:

        # If campus is not set show to all campuses
        if (not (notice.is_bothell or
                 notice.is_seattle or
                 notice.is_tacoma) or
                notice.is_seattle and affiliations['seattle'] or
                notice.is_bothell and affiliations['bothell'] or
                notice.is_tacoma and affiliations['tacoma']):
            campus_matched = True
        else:
            continue

        # If no affiliation is required
        if not (notice.is_alumni or notice.is_applicant or
                notice.is_grad or notice.is_grad_c2 or
                notice.is_pce or notice.is_student or
                notice.is_undergrad or notice.is_undergrad_c2 or
                notice.is_fyp or notice.is_past_student or
                notice.is_clinician or notice.is_employee or
                notice.is_faculty or notice.is_instructor or
                notice.is_past_employee or notice.is_retiree or
                notice.is_staff_employee or notice.is_stud_employee or
                notice.is_intl_stud):
            user_notices.append(notice)
            continue

        if notice.is_past_student and affiliations["past_stud"]:
            user_notices.append(notice)
            continue

        for key in affiliations:
            # exclude campuses
            if key == 'seattle' or key == 'bothell' or key == 'tacoma':
                continue
            try:
                if getattr(notice, "is_" + key) and affiliations[key]:
                    user_notices.append(notice)
                    continue
            except AttributeError:
                pass

    return user_notices
