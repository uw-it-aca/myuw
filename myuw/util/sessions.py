import logging
from django.contrib.sessions.models import Session
from django.utils import timezone

SCOPE_IDTOKEN = "idtoken"
logger = logging.getLogger(__name__)


def delete_sessions(netid, scope=None):
    """
    Delete all the live sessions of the netid in the specified scope
    Param scope value: SCOPE_IDTOKEN or None (all)
    """
    now = timezone.now()
    for session in Session.objects.filter(expire_date__gt=now):
        try:
            data = session.get_decoded()
            if _is_qualified(data, netid, scope) is True:
                session.delete()
                logger.info({'msg': "Deleted session of {}".format(netid),
                             'scope': scope})
        except Exception as ex:
            logger.error({'msg': "When deleting session of {}".format(netid),
                          'scope': scope,
                          'err': ex})


def _is_qualified(data, netid, scope):
    if scope == SCOPE_IDTOKEN:
        return (data.get('uw_oidc_idtoken') and
                data.get('_uw_original_user') == netid)
    return (data.get('_us_original_user') == netid or
            data.get('_uw_original_user') == netid or
            data.get('samlUserdata') and
            data['samlUserdata']['uwnetid'][0] == netid)
