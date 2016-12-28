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
    return Response('Hello World')


def app_factory(global_config, **local_config):
    return application


def main():
    logging.register_options(CONF)
    CONF(sys.argv[1:])
    logging.setup(CONF, 'vendordata')

    wsgi_app = loadapp('config:paste.ini', relative_to='.')
    httpserver.serve(wsgi_app, host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
