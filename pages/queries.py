"""Expose query page with a valid module name for tests."""

from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import pandas as pd


_spec = spec_from_file_location("pages.2_queries", Path(__file__).with_name("2_queries.py"))
_mod = module_from_spec(_spec)
_spec.loader.exec_module(_mod)  # type: ignore

# Expose key functions and variables so tests can patch them
q010_open_order_report_data = _mod.q010_open_order_report_data
q093_shipment_status = _mod.q093_shipment_status
query_descriptions = _mod.query_descriptions


def get_query_data():
    """Return data for available queries with basic error handling."""
    results = {}
    try:
        results["Open Order Report"] = q010_open_order_report_data()
    except Exception:
        results["Open Order Report"] = pd.DataFrame()

    try:
        results["Shipment Status"] = q093_shipment_status()
    except Exception:
        results["Shipment Status"] = pd.DataFrame()

    return results

import sys
sys.modules.setdefault("pages.queries", sys.modules[__name__])
