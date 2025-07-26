# ttu_open_report

This repository contains code and resources for the TTU Open Report project.

## Project Structure
- `extract.py`: Main extraction script
- `schema.json`: Database schema definition
- `models/`: Data models and query definitions
- `tests/`: Unit tests


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

### 3. Exporting data

Run the extraction pipeline:

```powershell
python extract.py `
  --db-path C:\AccessApps\ttu_open_report\Opnordrp-vlad-copy.accdb `
  --output-dir cache\raw `
  --schema-path schema.json
```

Check that `cache\raw\` is populated and `schema.json` updates.

### 4. Running tests

```powershell
pytest -q --disable-warnings
```

All tests must pass before proceeding.

### 5. Launching Streamlit

```powershell
streamlit run app.py
```

---

For more details, see the source code and documentation in this repository.
