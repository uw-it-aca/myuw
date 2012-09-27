from django.conf import settings
from datetime import datetime
import logging

""" Specify the log file of the myuw_mobile application """

app_name = 'myuw_mobile'
logfile_prefix = 'logs/' + app_name + '.'

logger = logging.getLogger(app_name)

if hasattr(settings, 'MYUW_LOG_FILE'):
    logfile_prefix = settings.'MYUW_LOG_FILE'
            
fhandler = logging.FileHandler(logfile_prefix +
                               datetime.strftime('%Y%m%d'))
fhandler.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s [%(name)s]')
fhandler.setFormatter(formatter)

logger.addHandler(fhandler)

    
