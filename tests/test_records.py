import io


def test_list_records(client):
    csv_content = (
        b"cmdCode,refYear,reporterDesc,partnerDesc,flowDesc,primaryValue\n"
        b"2204,2023,France,Japan,Export,1000\n"
    )
    fake_file = io.BytesIO(csv_content)

    upload_response = client.post(
        "/imports/files",
        files={"file": ("list.csv", fake_file, "text/csv")},
    )
    import_job_id = upload_response.json()["id"]

    response = client.get(f"/records?import_job_id={import_job_id}")

    assert response.status_code == 200
    records = response.json()
    assert len(records) == 1
    assert records[0]["content"]["cmdCode"] == 2204


def test_export_records(client):
    csv_content = (
        b"cmdCode,cmdDesc,refYear,reporterDesc,partnerDesc,flowDesc,primaryValue\n"
        b"2204,Wine of fresh grapes,2023,France,Japan,Export,1000\n"
    )
    fake_file = io.BytesIO(csv_content)

    client.post(
        "/imports/files",
        files={"file": ("export.csv", fake_file, "text/csv")},
    )

    response = client.get("/records/export?cmd_code=2204")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "2204" in response.text
    assert "France" in response.text