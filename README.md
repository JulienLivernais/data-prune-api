Data Prune API
----------
DataPrune is a dedicated data processing app focused on the ingestion, validation, 
cleaning and normalisation of heterogeneous data. It takes messy files from different sources (
CSV, Excel, JSON, PDF and API planned) and turns them into one clean, consistent
dataset: no duplicates, no missing or invalid values. The current example uses French
export data to Japan (wine, leather goods, cosmetics, technology), but the app works with
any type of data. The result is a clean dataset plus a report showing exactly what was
fixed.

Deployment
-----
This API is deployed on Railway. Swagger UI: https://data-prune-api-production.up.railway.app/docs

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

DATA SOURCES
-----
Focus: French exports to Japan: wine, leather goods, cosmetics/perfumes, and technology
(computing, aerospace, medical devices, semiconductors, telecom, industrial robotics).
- UN Comtrade: official bilateral trade statistics between France and Japan, by product

AVAILABLE PRODUCTS / HS CODES for export
-----
2204 - Wine
3304 - Cosmetics
4202 - Leather goods
8471 - Computers
8479 - Industrial machinery
8486 - Semiconductor manufacturing equipment
8517 - Telecom equipment, smartphones
8541 - Semiconductors
8542 - Integrated circuits
8802 - Aircraft
9018 - Medical devices

CI/CD
-----
GitHub Actions (CI) + Railway (CD)

STACK
-----
* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic2
* Pydantic
* Pandas

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

FUTURE IMPROVEMENTS
----------
- API import + PDF + Google Sheets import
- Authentication to secure endpoints (JWT)
- Visual representation of the data-quality report (Matplotlib), updated with the latest data injected

