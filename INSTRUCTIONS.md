# INSTRUCTIONS.md

## Project Overview
This project is a modular Python/Streamlit application for extracting, visualizing, and reporting on Access database tables. It includes:
- Extraction pipeline (`extract.py`)
- Dynamic schema loader (`models/table_schema.py`)
- Query logic and mock data (`models/query_definitions.py`)
- Streamlit multi-page UI (`pages/`)
- Unit tests (`tests/`)
- Sample data (`cache/raw/`)

## Setup Instructions
1. **Clone the repository**
2. **Install dependencies**
   - Use a virtual environment (recommended)
   - Run: `pip install -r requirements.txt`
3. **Configure environment variables**
   - Copy `.env.example` to `.env` and update credentials as needed
4. **Run the Streamlit app**
   - `streamlit run app.py`
5. **Run extraction**
   - `python extract.py --help` for options
6. **Run tests**
   - `pytest tests/`

## Sample Data
- Sample CSV exports are in `cache/raw/` for UI testing and development.
- The Access database file is `Opnordrp-vlad-copy.accdb` (for local extraction).

## UI Pages
- **Tables**: Select and preview tables, view schema, download CSV
- **Queries**: Select queries, view results, download CSV
- **Reports**: Visualize data, summary stats
- **Forms**: Feedback/sample forms

## Troubleshooting
- If you encounter DB connection issues, check `.env` and Access driver installation.
- For UI errors, ensure sample data is present in `cache/raw/`.

## Contributing
- Follow PEP8 for Python code
- Add unit tests for new features
- Update documentation as needed

## Contact
For support, contact TechopsTTU or open an issue in the repository.
