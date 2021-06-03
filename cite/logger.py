import logging
from inject_config import *
from django.core.handlers.wsgi import WSGIRequest as ReqClass

from cite.settings import DEBUG
LOG_EXCEPTION = not DEBUG


def view_log(view_f):
    def view_shell(request: ReqClass, **kwargs):
        login = ' '
        if 'user' in request.session.keys():
            login = request.session['user']['login']
        logging.info("user %s from %s requested url %s" %
                     (login, request.environ['REMOTE_ADDR'], request.environ['PATH_INFO']))
        if 'HTTP_REFERER' in request.environ.keys():
            logging.info('user redirected from %s' % request.environ['HTTP_REFERER'])

        if LOG_EXCEPTION:
            try:
                return view_f(request, **kwargs)
            except BaseException as ex:
                logging.exception("while processing %s (%s) exception %s raised: %s" %
                                  (view_f.__name__, request.environ['PATH_INFO'], ex.__class__, str(ex)))
        else:
            return view_f(request, **kwargs)

    return view_shell
