# GraphiteVision Analytics

GraphiteVision Analytics is a comprehensive business intelligence platform for Toyo Tanso USA, designed for extracting, visualizing, and reporting on manufacturing and operational data. It supports both mock/sample data and real database connections, enabling:
- Advanced data extraction and preview
- Business analytics and operational insights
- Interactive reports and charts
- Secure data entry portal

The application is specifically tailored for graphite manufacturing operations, providing teams with quick insights and comprehensive reporting capabilities.

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

To connect to the NdustrOS database instead of the bundled SQLite test DB,
set the following environment variables in your `.env`:

```bash
USE_SQLITE=false
NDUSTROS_USER=TTUSA\NDUSTROS
NDUSTROS_PASS=your_password_here
```

### 4. Running the app

- `streamlit run app.py` for the dashboard
- `python extract.py --help` for extraction options

### 5. Running tests

- `pytest` for unit tests (uses `pytest.ini` for options)
- `python -m unittest selenium_tests/test_tables_page.py` for UI tests
- Generate an HTML report with `pytest --html=reports/report.html --self-contained-html`

### 6. Containerized deployment

Build and run the application using Docker:

```bash
docker build -t graphitevision .
docker run -p 8501:8501 graphitevision
```

### 7. Continuous Integration

This repository includes a GitHub Actions workflow (`.github/workflows/ci.yml`)
that installs dependencies and runs the test suite on each push or pull request.

Check that `cache/raw/` is populated and `schema.json` updates.

See `INSTRUCTIONS.md` for full details, troubleshooting, and team onboarding.

---

For more details, see the source code and documentation in this repository.
