import logging
from inject_config import *
from django.core.handlers.wsgi import WSGIRequest as ReqClass


def view_log(view_f):
    def view_shell(request: ReqClass, **kwargs):
        login = ' '
        if 'user' in request.session.keys():
            login = request.session['user']['login']
        logging.info("user %s from %s requested url %s (redirected from %s)" %
                     (login, request.environ['REMOTE_ADDR'], request.environ['PATH_INFO'],
                      request.environ['HTTP_REFERER']))

        try:
            return view_f(request, **kwargs)
        except BaseException as ex:
            logging.exception("while processing %s (%s) exception %s raised: %s" %
                              (view_f.__name__, request.environ['PATH_INFO'], ex.__class__, str(ex)))

    return view_shell
