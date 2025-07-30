# INSTRUCTIONS.md

## Project Overview
TTU Open Report is a modular Python/Streamlit application for extracting, visualizing, and reporting on Access database tables. It supports both mock/sample data and real Access DB connections.

## Setup Instructions
1. **Clone the repository**
2. **Install dependencies**
   - Use a virtual environment (recommended)
   - Run: `pip install -r requirements.txt`
3. **Configure environment variables**
   - Copy `.env.example` to `.env` and fill in your credentials and Access DB path
   - Example:
     ```
     NDUSTROS_USER=TTUSA\NDUSTROS
     NDUSTROS_PASS=your_password_here
     ACCESS_DB_PATH=Opnordrp-vlad-copy.accdb
     ACCESS_DB_DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}
     ```
4. **Run the Streamlit app**
   - `streamlit run app.py`
5. **Run extraction**
   - `python extract.py --help` for options
6. **Run tests**
   - `pytest` (uses `pytest.ini` to generate an HTML report)
   - `python -m unittest selenium_tests/test_tables_page.py` for UI tests

## Mock Data & Sample Usage
- Sample CSVs are in `cache/raw/` for UI testing and development.
- The Access database file is `Opnordrp-vlad-copy.accdb` (for local extraction).
- Schema is defined in `schema.json` and matches sample data.

## Real DB Connection
- Ensure you have Access drivers installed (Windows: ODBC, `pyodbc`).
- Set `USE_SQLITE=false` in your `.env` to run queries against the NdustrOS
  database instead of the SQLite test DB.
- Provide `NDUSTROS_USER` and `NDUSTROS_PASS` credentials (and adjust
  `NDUSTROS_SERVER`, `NDUSTROS_PORT`, `NDUSTROS_DB`, and `NDUSTROS_DRIVER` if
  needed).
- Example:
  ```
  USE_SQLITE=false
  NDUSTROS_USER=TTUSA\NDUSTROS
  NDUSTROS_PASS=your_password_here
  ```
- Test the connection using the utility in `models/query_definitions.py`.

## Troubleshooting
- **DB Connection Issues:**
  - Check `.env` and Access driver installation.
  - Use mock/sample data for UI testing if DB is unavailable.
  - Missing `NDUSTROS_USER` or `NDUSTROS_PASS` will raise a `ValueError`
    in `models/query_definitions.py` when building the connection string.
- **UI Errors:**
  - Ensure sample data is present in `cache/raw/`.
  - Run tests to validate extraction and schema mapping.

## Team Onboarding Checklist
- [ ] Clone repo and set up virtual environment
- [ ] Install dependencies
- [ ] Copy `.env.example` to `.env` and fill in credentials
- [ ] Run Streamlit app and verify UI with mock/sample data
- [ ] Run all tests (unit and UI)
- [ ] Update `.env` for real DB access when available

## Contributing
- Follow PEP8 for Python code
- Add unit/UI tests for new features
- Update documentation as needed

## Contact
For support, contact TechopsTTU or open an issue in the repository.
