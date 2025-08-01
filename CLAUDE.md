# Project Instructions for Claude

## Project Overview
GraphiteVision Analytics - Business intelligence platform for Toyo Tanso USA, a graphite manufacturing company. Built with Streamlit for web interface, handles manufacturing and operational data.

## Project Structure
- `app.py` - Main Streamlit application
- `extract.py` - Data extraction functionality 
- `pages/` - Multiple report pages including Open Order Report
- `models/` - Data models and query definitions
- `tests/` - Comprehensive test suite (unit tests, Playwright, Selenium)
- `cache/raw/` - Sample CSV data files

## Development Setup
1. Set up virtual environment: `python -m venv .venv && .\.venv\Scripts\Activate.ps1`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `.env` file with credentials
4. Run the app: `streamlit run app.py`

## Testing
- Unit tests: `python -m pytest tests/`
- Playwright tests: `python -m pytest tests/test_playwright.py`
- Selenium tests: `python -m pytest tests/test_selenium.py`

## Git Workflow
- Main branch: `main`
- Current branch: `dev`
- Recent commits show active development on Open Orders report and testing infrastructure

## Code Standards
- Follow existing Python conventions in the codebase
- Use existing libraries and utilities found in the project
- Follow security best practices - never expose or log secrets
- Maintain existing code style and patterns