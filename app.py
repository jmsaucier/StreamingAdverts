from flask import Flask
import ConfigParser

# If you get an error on the next line on Python 3.4.0, change to: Flask('app')
# where app matches the name of this file without the .py extension.
app = Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

def ParseConfig(app):
    config = ConfigParser.ConfigParser()
    config.read('settings.ini')
    app.config['OAuth_ClientID'] = config.get('ApplicationSettings','OAuth_ClientID')
    app.config['OAuth_ClientSecret'] = config.get('ApplicationSettings','OAuth_ClientSecret')
    app.config['OAuth_RedirectUrl'] = config.get('ApplicationSettings', 'OAuth_RedirectUrl')
    app.config['OAuth_PostUrl'] = config.get('ApplicationSettings', 'OAuth_PostUrl')
    app.config['OAuth_CallbackUrl'] = config.get('ApplicationSettings', 'OAuth_CallbackUrl')
    app.secret_key = config.get('ApplicationSettings', 'Secret_Key')
    app.config['port'] = config.get('ApplicationSettings', 'port')
    app.config['host'] = config.get('ApplicationSettings', 'host')

from routes import *
ParseConfig(app)
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app

if __name__ == '__main__':
    import os
    host = os.environ.get('SERVER_HOST', 'localhost')
    try:
        port = int(os.environ.get('SERVER_PORT', app.config['port']))
    except ValueError:
        port = 5555
    app.run(host, port)
