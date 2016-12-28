#!/usr/bin/python

# An example vendordata server implementation for OpenStack Nova. With a giant
# nod in the direction of Chad Lung for his very helpful blog post at
# http://www.giantflyingsaucer.com/blog/?p=4701

from webob import Response
from webob.dec import wsgify
from paste import httpserver
from paste.deploy import loadapp
 
 
@wsgify
def application(req):
    return Response('Hello World')
 
 
def app_factory(global_config, **local_config):
    return application
 
 
wsgi_app = loadapp('config:paste.ini', relative_to='.')
httpserver.serve(wsgi_app, host='127.0.0.1', port=8080)
