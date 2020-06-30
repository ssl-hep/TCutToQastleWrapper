#!/usr/bin/env python

"""
TCut selection for ROOT TTree to Qastle wrapper for ServiceX xAOD and Uproot transformer

Usage:
    import tcut_to_qastle
    query = tcut_to_qastle.translate(<TCut selection>, <Columns to deliver>)
"""

from .translate import translate, get_list_of_columns_in_selection