#!/usr/bin/env python
"""
    demo.py
    ~~~~~~~

    :copyright: (c) 2011 - Stephane Wirtel <stephane@wirtel.be>
    :license: BSD License

"""
from flask import Flask
from flask import g, json, Response
from flask.ext.openerp import OpenERP, get_object

class DefaultConfig(object):
    OPENERP_SERVER = 'http://localhost:8069'
    OPENERP_DATABASE = 'oerp5'
    OPENERP_DEFAULT_USER = 'admin'
    OPENERP_DEFAULT_PASSWORD = 'admin'

    SECRET_KEY = 'secret_key'

    DEBUG = True

app = Flask(__name__)
app.config.from_object(DefaultConfig())
OpenERP(app)

@app.route('/')
def index():
    proxy = get_object('res.users')
    users = proxy.read([], ['name', 'login'])
    return Response(json.dumps(users), mimetype='application/json')

app.run(debug=True)
