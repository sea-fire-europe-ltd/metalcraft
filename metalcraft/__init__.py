# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from erpnext.stock.doctype.batch import batch
from . import overrides

__version__ = '0.0.1'

batch._make_naming_series_key = overrides._make_naming_series_key
