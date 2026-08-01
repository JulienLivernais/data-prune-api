DataPrune API
----------
DataPrune is a data cleaning app. It takes messy files from different sources (
CSV, Excel, JSON, PDF and API planned) and turns them into one clean, consistent
dataset: no duplicates, no missing or invalid values. The current example uses French
export data to Japan (wine, leather goods, cosmetics, technology), but the app works with
any type of data. The result is a clean dataset plus a report showing exactly what was
fixed.

WHY A CUSTOM CLEANING PIPELINE
-----
- Different sources, one cleaning engine: source-specific importers convert incoming
  data (customs statistics, invoices, market reports) into a common internal representation,
  then a single reusable pipeline validates, cleans and normalises it
- Every import is traceable through a quality report (input records, values corrected,
  duplicates removed, rejected records)
- Processing runs in the background (FastAPI BackgroundTasks), so the API responds immediately
  instead of blocking on large files
- Source fingerprints prevent the same file from being processed twice

DATA SOURCES
-----
Focus: French exports to Japan: wine, leather goods, cosmetics/perfumes, and technology
(computing, aerospace, medical devices, semiconductors, telecom, industrial robotics).
- UN Comtrade: official bilateral trade statistics between France and Japan, by product
- Japan Customs / e-Stat: Japanese import statistics by commodity and country of origin

STACK
-----
* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Pydantic
* Pandas
* Docker
* Pytest

DATABASE
-----
import_job
* id, source_type, filename, file_path, fingerprint, status, created_at, completed_at

record
* id, content (JSONB), status, rejection_reason, import_job_id

quality_report
* id, input_records, rejected_records, values_corrected, duplicates_removed, import_job_id

SETUP IN LOCAL
-----
1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies: pip install -r requirements.txt
4. Copy .env.example to .env and fill in the values
5. Create the PostgreSQL database
6. Run migrations: alembic upgrade head
7. Start the server: uvicorn app.main:app --reload
8. Open API docs: http://localhost:8000/docs

FUTURE IMPROVEMENTS
----------
- Excel import + JSON / API import + PDF import  
- Google Sheets import support
- Add tests with Pytest
- Authentication to secure endpoints (JWT)
- Visual representation of the data-quality report (Matplotlib), updated with the latest data injected
- Docker setup 
