# -*- coding: utf-8 -*-
"""
    config for webget

    :copyright: 20150811 by raptor.zh@gmail.com.
"""

from os.path import dirname, abspath, expanduser, join as joinpath
import json

import logging

logger = logging.getLogger(__name__)


config_default = {
    "down_dir": "~/down",
    "wget_dir": "/usr/local/bin",
    "web_down": "/wget/static/down",
    "web_path": "wget",
    "web_addr": "127.0.0.1",
    "web_port": 8111,
    "debug": False,
}


def get_fullname(*args):
    root = dirname(abspath(__file__))
    return joinpath(root, joinpath(*args)) if len(args) > 0 else root


try:
    with open(get_fullname("config.json"), "r"):
        config = json.loads(read())
    config_default.update(config)
    config = config_default
except IOError:
    config = config_default

config['down_dir'] = expanduser(config['down_dir'])
