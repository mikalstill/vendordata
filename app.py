#!/usr/bin/python

# An example vendordata server implementation for OpenStack Nova. With a giant
# nod in the direction of Chad Lung for his very helpful blog post at
# http://www.giantflyingsaucer.com/blog/?p=4701

import json
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
    if req.environ.get('HTTP_X_IDENTITY_STATUS') != 'Confirmed':
        return Response('User is not authenticated', status=401)

    try:
        data = req.environ.get('wsgi.input').read()
        if not data:
            return Response('No data provided', status=500)

        # Get the data nova handed us for this request
        #
        # An example of this data:
        # {
        #     "hostname": "foo", 
        #     "image-id": "75a74383-f276-4774-8074-8c4e3ff2ca64", 
        #     "instance-id": "2ae914e9-f5ab-44ce-b2a2-dcf8373d899d", 
        #     "metadata": {}, 
        #     "project-id": "039d104b7a5c4631b4ba6524d0b9e981", 
        #     "user-data": null
        # }
        indata = json.loads(data)

        # We need to make up a response. This is where your interesting thing
        # would happen. However, I don't have anything interesting to do, so
        # I just return Carrie Fisher quotes instead.

        quotes = {'0': 'Instant gratification takes too long.',
                  '1': ('Resentment is like drinking poison and waiting for '
                        'the other person to die.'),
                  '2': ('I was street smart, but unfortunately the street was '
                        'Rodeo Drive.'),
                  '3': ('You can\'t find any true closeness in Hollywood, '
                        'because everybody does the fake closeness so well.'),
                  '4': ('As you get older, the pickings get slimmer, but the '
                        'people don\'t.'),
                  '5': ('There is no point at which you can say, "Well, I\'m '
                        'successful now. I might as well take a nap."'),
                  '6': ('I really love the internet. They say chat-rooms are '
                        'the trailer park of the internet but I find it '
                        'amazing.'),
                  '7': ('I don\'t think Christmas is necessarily about '
                        'things. It\'s about being good to one another, it\'s '
                        'about the Christian ethic, it\'s about kindness.'),
                  '8': ('I don\'t want my life to imitate art, I want my '
                        'life to be art.'),
                  '9': ('I am a spy in the house of me. I report back from '
                        'the front lines of the battle that is me. I am '
                        'somewhat nonplused by the event that is my life.'),
                  'a': 'I drowned in moonlight, strangled by my own bra.',
                  'b': 'Even in space there\'s a double standard for women.',
                  'c': ('Everyone drives somebody crazy. I just have a bigger '
                        'car.'),
                  'd': ('Sometimes you can only find Heaven by slowly '
                        'backing away from Hell.'),
                  'e': 'I\'m thinking of having my DNA fumigated.',
                  'f': 'Leia follows me like a vague smell.'
        }
        outdata = {'carrie_says': quotes[indata['instance-id'][-1]]}
        return Response(json.dumps(outdata, indent=4, sort_keys=True))

    except Exception as e:
        return Response('Server error while processing request: %s' % e,
                        status=500)


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
    httpserver.serve(wsgi_app, host='0.0.0.0', port=8888)


if __name__ == '__main__':
    main()
