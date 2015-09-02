# -*- coding: utf-8 -*-
"""
    botas params
    ~~~~~~~~~~~~~~~~

    params plugins for bottle.

    :copyright: 20150426 by raptor.zh@gmail.com.
    2015-09-02 for python3
"""
import inspect
import bottle

from webexceptions import WebBadrequestError

import logging

logger = logging.getLogger(__name__)


# PluginError is defined in bottle >= 0.10
if not hasattr(bottle, 'PluginError'):
    class PluginError(bottle.BottleException):
        pass
    bottle.PluginError = PluginError


class ParamsPlugin(object):

    name = 'params'
    api = 2

    def __init__(self, json_params=False, encoding='utf-8'):
        self.json_params = json_params
        self.encoding = encoding

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, ParamsPlugin):
                continue
            raise bottle.PluginError("Found another ParamsPlugin be installed.")
    
    def apply(self, callback, route):
        pluginconf = route.config
        _json_params = pluginconf.get("json_params", self.json_params)

        argspec = inspect.getargspec(route.callback)

        def wrapper(*args, **kwargs):
            try:
                if _json_params:
                    kw = bottle.request.json
                else:
                    if route.method == "POST" or route.method == "PUT":
                        kw = bottle.request.forms
                    else:
                        kw = bottle.request.query
            except:
                kw = None
            if kw:
                keys = set(kw.keys()) if argspec.keywords else set(kw.keys()).intersection(set(argspec.args[len(args):]))
                [kwargs.__setitem__(k,kw.__getattr__(k)) for k in keys]
            try:
                return callback(*args, **kwargs)
            except TypeError:
                import traceback
                logger.debug(traceback.format_exc())
                raise WebBadrequestError

        return wrapper
