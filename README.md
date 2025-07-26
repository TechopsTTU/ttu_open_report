# ttu_open_report

TTU Open Report is a modular Python/Streamlit application for extracting, visualizing, and reporting on Access database tables. It supports both mock/sample data and real Access DB connections, enabling:
- Data extraction and preview
- Business queries and analytics
- Interactive reports and charts
- Data entry forms

The app is designed for teams needing quick insights and reporting from Access databases, with robust testing and easy onboarding.

## Project Structure
- `extract.py`: Main extraction script
- `schema.json`: Database schema definition
- `models/`: Data models and query definitions
- `pages/`: Streamlit UI pages
- `selenium_tests/`: Automated UI tests
- `tests/`: Unit tests
- `cache/raw/`: Sample/mock CSVs for UI and testing


## Setup & Usage

### 1. Setting up the virtual environment

Open PowerShell in the project root and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Installing dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configuring environment variables

Copy `.env.example` to `.env` and fill in your credentials and Access DB path.

### 4. Running the app

- `streamlit run app.py` for the dashboard
- `python extract.py --help` for extraction options

### 5. Running tests

- `pytest tests/` for unit tests
- `python -m unittest selenium_tests/test_tables_page.py` for UI tests
- `pytest --maxfail=3 --disable-warnings`

Check that `cache/raw/` is populated and `schema.json` updates.

See `INSTRUCTIONS.md` for full details, troubleshooting, and team onboarding.

---

For more details, see the source code and documentation in this repository.
