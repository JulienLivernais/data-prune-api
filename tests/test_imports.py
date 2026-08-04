import io


def test_upload_csv(client):
    csv_content = (
        b"cmdCode,refYear,reporterDesc,partnerDesc,flowDesc,primaryValue\n"
        b"2204,2023,France,Japan,Export,1000\n"
    )
    fake_file = io.BytesIO(csv_content)

    response = client.post(
        "/imports/files",
        files={"file": ("test.csv", fake_file, "text/csv")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["source_type"] == "csv"
    assert data["status"] == "pending"
    assert data["filename"] == "test.csv"


def test_upload_wrong_type(client):
    fake_file = io.BytesIO(b"just some text")

    response = client.post(
        "/imports/files",
        files={"file": ("test.txt", fake_file, "text/plain")},
    )

    assert response.status_code == 400


def test_upload_duplicate(client):
    csv_content = b"cmdCode,refYear,reporterDesc,partnerDesc,flowDesc,primaryValue\n2204,2023,France,Japan,Export,1000\n"

    first_response = client.post(
        "/imports/files",
        files={"file": ("test.csv", io.BytesIO(csv_content), "text/csv")},
    )
    assert first_response.status_code == 200

    second_response = client.post(
        "/imports/files",
        files={"file": ("test.csv", io.BytesIO(csv_content), "text/csv")},
    )
    assert second_response.status_code == 409