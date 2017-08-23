#!/usr/bin/env python
"""
    openerp.py
    ~~~~~~~~~~
    :copyright: (c) 2010-2011 Stephane Wirtel <stephane@wirtel.be>
    :license: BSD
"""
from __future__ import absolute_import

from flask import _request_ctx_stack
from flask import session
from flask import g
from flask import abort

from erppeek import Client


__all__ = ['OpenERP', 'get_object', 'get_data_from_record']


def get_object(object_name):
    return g.openerp_cnx.model(object_name)


def get_data_from_record(object_name, record_ids, fields=None):
    if fields is None:
        fields = []

    proxy = get_object(object_name)
    records = proxy.read(record_ids, fields)

    if not records:
        abort(404)

    return records


class OpenERP(object):
    """
    This class is used to interact with an OpenERP Server to one or more Flask
    applications.

    There are two usage modes with work very similar. One is binding
    the instance to a very specific Flask application::

        app = Flask(__name__)
        openerp = OpenERP(app)

    The second possibility is to create the object once and configure
    the application later to support it::

        openerp = OpenERP()

        def create_ap():
            app = Flask(__name__)
            openerp.init_app(app)
            return app
    """
    def __init__(self, app=None):
        self.default_user = None
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        """This callback can be used to initialize an application for use with
        the OpenERP server.
        """
        app.config.setdefault('OPENERP_SERVER', 'http://localhost:8069')
        app.config.setdefault('OPENERP_DATABASE', 'openerp')
        app.config.setdefault('OPENERP_DEFAULT_USER', 'admin')
        app.config.setdefault('OPENERP_DEFAULT_PASSWORD', 'admin')

        app.jinja_env.globals.update(
            get_data_from_record=get_data_from_record
        )

        cnx = Client(
            server=app.config['OPENERP_SERVER'],
            db=app.config['OPENERP_DATABASE'],
            user=app.config['OPENERP_DEFAULT_USER'],
            password=app.config['OPENERP_DEFAULT_PASSWORD']
        )

        self.default_user = cnx.user

        app.before_request(self.before_request)

    def before_request(self):
        user = session.get('openerp_user', self.default_user)

        password = session.get('openerp_password',
                               self.app.config['OPENERP_DEFAULT_PASSWORD'])

        g.openerp_cnx = Client(
            server=self.app.config['OPENERP_SERVER'],
            db=self.app.config['OPENERP_DATABASE'],
            user=user,
            password=password
        )

    def __repr__(self):
        app = None

        if self.app is not None:
            app = self.app
        else:
            ctx = _request_ctx_stack.top
            if ctx is not None:
                app = ctx.app
        return '<%s openerp=%r>' % (
            self.__class__.__name__,
            app and "{0}/{1}".format(
                app.config['OPENERP_SERVER'], app.config['OPENERP_DATABASE']
            ) or ''
        )

    def login(self, username, password):
        c = Client(self.app.config['OPENERP_SERVER'])
        return c.login(username, password, self.app.config['OPENERP_DATABASE'])
