#!/usr/bin/env python

"""
TCut selection for ROOT TTree to Qastle wrapper for Uproot transformer

Usage:
    import tcut_to_qastle
    query = tcut_to_qastle.translate(<Tree Name>, <Columns to deliver>, <TCut selection>)
"""

from .translate import translate, get_list_of_columns_in_selection

__version__ = '0.4'