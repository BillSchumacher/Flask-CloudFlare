# -*- coding: utf-8 -*-
# Copyright (C) 2019 by Bill Schumacher
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby
# granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

from flask import current_app
from pycflare import CloudFlare as PyCloudFlare
from werkzeug.local import LocalProxy

cloudflare = LocalProxy(lambda: current_app.extensions['cloudflare'])


class CloudFlare(object):
    def __init__(self, app=None):
        self.app = app
        self.cf = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        auth_email = app.config.get('CLOUDFLARE_AUTH_EMAIL')
        auth_key = app.config.get('CLOUDFLARE_AUTH_KEY')
        redis_compat = app.config.get('CLOUDFLARE_ENABLE_REDIS_COMPATIBILITY', False)
        if auth_key is None or auth_email is None:
            raise RuntimeError("You must provide your CloudFlare AUTH_EMAIL and AUTH_KEY via CLOUDFLARE_AUTH_EMAIL and "
                               "CLOUDFLARE_AUTH_KEY in the app.config.")
        self.cf = PyCloudFlare(auth_email=auth_email, auth_key=auth_key, enable_redis_compatibility=redis_compat)
        app.extensions['cloudflare'] = self

    def register_account(self, account_id, name):
        return self.cf.register_account(account_id, name)

    def __getattr__(self, item):
        try:
            return self.cf.__getattribute__(item)
        except AttributeError:
            print("CloudFlare: Attribute {value} was not found.".format(value=item))
        return None
