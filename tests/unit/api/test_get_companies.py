from app.models.company import Company
from app.db import db


def create_test_companies():
    # Create test companies in the database
    test_companies = [
        Company(
            cnpj="12345678901234",
            nome_razao="Company A",
            nome_fantasia="A",
            cnae="1234567",
        ),
        Company(
            cnpj="23456789012345",
            nome_razao="Company B",
            nome_fantasia="B",
            cnae="2345678",
        ),
        Company(
            cnpj="34567890123456",
            nome_razao="Company C",
            nome_fantasia="C",
            cnae="3456789",
        ),
    ]
    db.session.add_all(test_companies)
    db.session.commit()


def test_get_companies_no_params(client, db):
    # Test getting all companies without any query parameters
    create_test_companies()

    response = client.get("/companies")

    assert response.status_code == 200
    assert len(response.json) == 3  # Assuming 3 test companies were created


def test_get_companies_with_params(client, db):
    # Test getting companies with query parameters
    create_test_companies()

    response = client.get("/companies?sort=cnpj&limit=1&start=0&dir=ASCENDING")

    assert response.status_code == 200
    assert len(response.json) == 1  # Expecting only one company
    assert (
        response.json[0]["cnpj"] == "12345678901234"
    )  # Assuming this is the first company when sorted by CNPJ ascending


def test_get_companies_invalid_params(client):
    # Test getting companies with invalid query parameters
    response = client.get("/companies?sort=invalid_field")

    assert response.status_code == 400


def test_get_companies_pagination(client, db):
    # Test pagination by limiting and starting from a specific index
    create_test_companies()

    response = client.get("/companies?limit=1&start=1")

    assert response.status_code == 200
    assert len(response.json) == 1  # Expecting only one company
    assert (
        response.json[0]["cnpj"] == "23456789012345"
    )  # Assuming this is the second company when sorted by primary key


def test_get_companies_sort_descending(client, db):
    # Test sorting companies in descending order
    create_test_companies()

    response = client.get("/companies?sort=cnpj&dir=DESCENDING")

    assert response.status_code == 200
    assert len(response.json) == 3
    assert (
        response.json[0]["cnpj"] == "34567890123456"
    )  # Assuming this is the highest CNPJ when sorted in descending order


def test_get_companies_invalid_sort_field(client):
    # Test getting companies with invalid sort field
    response = client.get("/companies?sort=invalid_field")

    assert response.status_code == 400


def test_get_companies_invalid_dir(client):
    # Test getting companies with invalid sort direction
    response = client.get("/companies?dir=INVALID")

    assert response.status_code == 400
