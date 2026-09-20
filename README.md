Data Prune API
----------

[![CI](https://github.com/JulienLivernais/data-prune-api/actions/workflows/ci.yml/badge.svg)](https://github.com/JulienLivernais/data-prune-api/actions/workflows/ci.yml)

DataPrune is a FastAPI service that ingests trade data files (CSV, Excel, JSON), cleans and validates them, 
and exports the result as CSV. It currently supports two sources, UN Comtrade and Japan Customs, 
each processed with its own validation rules and export format. The case study covers French exports to 
Japan (wine, leather goods, cosmetics, technology). Each import produces a quality report: input records, 
rejected records, duplicates removed and values corrected.

Deployment
-----
This API is deployed on Railway. Swagger UI: https://data-prune-api-production.up.railway.app/docs

CI/CD
-----
GitHub Actions (CI) + Railway (CD)

WHY A CUSTOM CLEANING PIPELINE
-----
- Different sources, one cleaning engine: source-specific importers convert incoming files
  into a common format, then a single pipeline validates, cleans and normalises the data
- Every import is traceable through a quality report (input records, values corrected,
  duplicates removed, rejected records)
- Processing runs in the background (FastAPI BackgroundTasks), so the API responds right
  away instead of waiting on large files
- Source fingerprints stop the same file from being processed twice
- Cleaned records can be exported as CSV, filtered by product or year

MULTI-SOURCE ARCHITECTURE
-----
- Same pipeline, different sources: structures are detected automatically, no manual config
- Each source (UN Comtrade, Japan Customs) has its own validation, business rules, and export columns
- Records from all sources share the same database table (PostgreSQL JSONB)
- Records are exported separately per source (un_comtrade or japan_customs)

DATA SOURCES
-----
Focus: French exports to Japan: wine, leather goods, cosmetics/perfumes, and technology
(computing, aerospace, medical devices, semiconductors, telecom, industrial robotics).
- UN Comtrade: official bilateral trade statistics between France and Japan, by product 
- Japan Customs / e-Stat: Japanese import statistics by commodity and country of origin

AVAILABLE PRODUCTS / HS CODES for export (UN Comtrade export)
-----
* 2204 - Wine
* 3304 - Cosmetics
* 4202 - Leather goods
* 8471 - Computers
* 8479 - Industrial machinery
* 8486 - Semiconductor manufacturing equipment
* 8517 - Telecom equipment, smartphones
* 8541 - Semiconductors
* 8542 - Integrated circuits
* 8802 - Aircraft
* 9018 - Medical devices

RECORDS EXPORT
-----
Cleaned records can be downloaded as CSV files, one export per source.
- Choose a source: un_comtrade or japan_customs
- Each source has its own columns in the exported file
- For UN Comtrade, results can also be filtered by product, product code, or year

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

SETUP WITH DOCKER
-----
1. Clone the repository: git clone https://github.com/JulienLivernais/data-prune-api
2. Navigate to the project: cd data-prune-api
3. Copy the environment file and fill in the values: cp .env.example .env
4. Build and start the containers: docker compose up --build
5. Run database migrations: docker compose exec app alembic upgrade head
6. Open API docs: http://localhost:8001/docs
7. Stop the containers when done: docker compose down


