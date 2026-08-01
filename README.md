DataPrune API
----------
DataPrune is a dedicated data processing app focused on the ingestion, validation, cleaning
and normalisation of heterogeneous data. It brings together files from variable sources
(CSV, Excel, JSON, PDF, API) and turns them into a single, coherent dataset: consistent formats, no duplicates,
no missing or invalid values. The current use case focuses on French exports to Japan 
(wine, leather goods, cosmetics/perfumes, and technology), 
but the pipeline itself is source-agnostic and works with any heterogeneous dataset. 
The result is a clean, ready-to-use dataset together with a traceable
data-quality report showing exactly what was fixed.

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

- UN Comtrade — official bilateral trade statistics between France and Japan, by product
  (HS code), value and quantity > CSV export or API (JSON).
- Japan Customs / e-Stat — Japanese import statistics by commodity and country of origin,
  published monthly by the Ministry of Finance > CSV
- University of Adelaide — Annual Database of Global Wine Markets, covering wine production
  and consumption by country, including France and Japan > Excel
- Wine Institute / IWSC — sample commercial export invoices for wine shipments, including
  HS codes, quantities and destination country > PDF

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
1. Clone the repository: git clone https://github.com/JulienLivernais/dataprune-app
2. Navigate to the project: cd dataprune-app
3. Copy the environment file and fill in the values: cp .env.example .env
4. Build and start the containers: docker compose up --build
5. Run database migrations: docker compose exec app alembic upgrade head
6. Open API docs: http://localhost:8000/docs
7. Stop the containers when done: docker compose down

FUTURE IMPROVEMENTS
----------
- PDF + API + Google Sheets > import 
- Add tests with Pytest
- Authentication to secure endpoints (JWT)
- Visual representation of the data-quality report (Matplotlib), updated with the latest data injected

