import logging
import logging.handlers

""" Specify the log file of the myuw_mobile application """

app_name = 'myuw_mobile'
log_dir = 'logs/'
logfile_prefix = log_dir + app_name

logger = logging.getLogger(app_name)

fhandler = logging.handlers.TimedRotatingFileHandler(logfile_prefix,
                                                     when='midnight')
fhandler.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s %(asctime)s %(user)s %(message)s [%(name)s]')
                              )
fhandler.setFormatter(formatter)

logger.addHandler(fhandler)
