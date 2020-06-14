#!/usr/bin/env python

"""
TCut selection for ROOT TTree to Qastle wrapper for ServiceX xAOD and Uproot transformer

Usage:
    import tcut_to_qastle
    tq = tcut_to_qastle.Translate(<TCut selection>, <Columns to deliver>)
    query = tq.to_qastle()

"""

from .translate import Translate

__all__ = ["to_qastle", "list_of_columns_in_selection", "tcut_selection", "selected_columns"]