import io

from app.models.import_job import ImportJob, SourceType, Status


def test_report_not_found(client):
    response = client.get("/reports/999")

    assert response.status_code == 404


def test_report_still_processing(client, db_session):
    import_job = ImportJob(
        source_type=SourceType.csv,
        filename="pending.csv",
        file_path="uploads/pending.csv",
        fingerprint="fake-fingerprint-pending",
        status=Status.pending,
    )
    db_session.add(import_job)
    db_session.commit()
    db_session.refresh(import_job)

    response = client.get(f"/reports/{import_job.id}")

    assert response.status_code == 202
    assert response.json() == {"status": "processing"}


def test_report_finished(client):
    csv_content = (
        b"cmdCode,refYear,reporterDesc,partnerDesc,flowDesc,primaryValue\n"
        b"2204,2023,France,Japan,Export,1000\n"
    )
    fake_file = io.BytesIO(csv_content)

    upload_response = client.post(
        "/imports/files",
        files={"file": ("finished.csv", fake_file, "text/csv")},
    )
    import_job_id = upload_response.json()["id"]

    response = client.get(f"/reports/{import_job_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["input_records"] == 1
    assert data["import_job_id"] == import_job_id