import os
import pytest
import pandas as pd
from src.models.query_definitions import get_db_connection, get_open_orders_report

@pytest.mark.skipif(os.environ.get('DATABASE_ENV') != 'pervasive', reason="Skipping Pervasive DB tests")
class TestPervasiveIntegration:
    def test_pervasive_connection(self):
        """Tests that a connection can be established with the Pervasive database."""
        conn = get_db_connection()
        assert conn is not None
        conn.close()

    def test_get_open_orders_report_pervasive(self):
        """
        Tests the get_open_orders_report function against the Pervasive database.
        This is a key integration test.
        """
        # Using a wide date range to ensure we get some data if the DB is populated.
        start_date = '2020-01-01'
        end_date = '2025-12-31'
        
        df = get_open_orders_report(start_date, end_date)
        
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert not df.empty, "The Open Orders report returned no data. This could be an error or just no data in the date range."
