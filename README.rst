This is a simple example of a Nova vendordata external server which uses
the keystone auth WSGI middleware. It was written to test the Nova vendordata
implementation.

The contents here are laid out as follows:

- requirements.txt: python dependancies for this code. Install this to your
  venv before trying this out

- app.py: the vendordata server code. This is mostly where you should add your
  useful local thing.

- paste.ini: the WSGI paste configuration for the server. You might want to
  tweak this to turn off debugging.

There is also credentials.json which is keystone credentials for your test
requests. Tweak this to contain values which are valid for your local
deployment and then use curl to fetch an auth token like this:

$ curl -d @credentials.json -H "Content-Type: application/json" http://172.29.236.100:5000/v2.0/tokens > token.json

Where 172.29.236.100 is the IP of your keystone deployment. This will give you
a keystone token as a JSON file called token.json. Extract from that your
token id, and you're good to make test requests against this server:

$ cat token.json | python -c "import sys, json; print json.loads(sys.stdin.read())['access']['token']['id'];"

