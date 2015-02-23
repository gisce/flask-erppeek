#!/usr/bin/env python
"""
    demo.py
    ~~~~~~~

    :copyright: (c) 2011 - Stephane Wirtel <stephane@wirtel.be>
    :license: BSD License

"""
from flask import Flask
from flask import g
from flask.ext.openerp import OpenERP


class DefaultConfig(object):
    OPENERP_PROTOCOL = 'xmlrpc'
    OPENERP_HOSTNAME = 'localhost'
    OPENERP_DATABASE = 'openrp'
    OPENERP_DEFAULT_USER = 'admin'
    OPENERP_DEFAULT_PASSWORD = 'admin'
    OPENERP_PORT = 8069

    SECRET_KEY = 'secret_key'

    DEBUG = True

app = Flask(__name__)
app.config.from_object(DefaultConfig())
OpenERP(app)


@app.route('/')
def index():

    sale_obj = g.openerp_cnx.model('sale.order')
    so_id = sale_obj.search([('state', '=', 'draft')], limit=1)
    
    g.openerp_cnx.exec_workflow('sale.order', 'order_confirm', so_id[0])

    return ""

app.run()

