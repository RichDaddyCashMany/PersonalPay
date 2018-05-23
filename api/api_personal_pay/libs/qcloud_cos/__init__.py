#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libs.qcloud_cos.cos_auth import Auth
from libs.qcloud_cos.cos_cred import CredInfo


import logging

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
