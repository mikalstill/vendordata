#!/usr/bin/python

# An example vendordata server implementation for OpenStack Nova. With a giant
# nod in the direction of Chad Lung for his very helpful blog post at
# http://www.giantflyingsaucer.com/blog/?p=4701

import sys

from webob import Response
from webob.dec import wsgify
from paste import httpserver
from paste.deploy import loadapp

from oslo_config import cfg
from oslo_log import log as logging


CONF = cfg.CONF
LOG = logging.getLogger(__name__)

@wsgify
def application(req):
    LOG.debug('Application ran')
    return Response('Hello World')


def app_factory(global_config, **local_config):
    return application


def main():
    logging.register_options(CONF)

    # Make keystonemiddleware emit debug logs
    extra_default_log_levels = ['keystonemiddleware=DEBUG']
    logging.set_defaults(default_log_levels=(logging.get_default_log_levels() +
                                             extra_default_log_levels))

    # Parse our config
    CONF(sys.argv[1:])

    # Set us up to log as well
    logging.setup(CONF, 'vendordata')

    # Start the web server
    wsgi_app = loadapp('config:paste.ini', relative_to='.')
    httpserver.serve(wsgi_app, host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
