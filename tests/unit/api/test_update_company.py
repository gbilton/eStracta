from uuid import uuid4

from app.db import db
from app.models.company import Company


def create_test_company():
    # Create a test company in the database
    test_company = Company(
        id=uuid4(),
        cnpj="12345678901234",
        nome_razao="Test Company",
        nome_fantasia="Test",
        cnae="1234567",
    )
    db.session.add(test_company)
    db.session.commit()
    return test_company.id


def test_update_company_success(client, db):
    # Test updating a company with valid data
    company_id = create_test_company()
    data = {"nome_fantasia": "Updated Name", "cnae": "8765432"}

    response = client.patch(f"/companies/{company_id}", data=data)

    assert response.status_code == 200
    assert response.json["nome_fantasia"] == "Updated Name"
    assert response.json["cnae"] == "8765432"


def test_update_company_missing_data(client, db):
    # Test updating a company with missing data
    company_id = create_test_company()
    data = {}  # Missing required fields

    response = client.patch(f"/companies/{company_id}", data=data)

    assert response.status_code == 400


def test_update_company_invalid_data(client, db):
    # Test updating a company with invalid data
    company_id = create_test_company()
    data = {"nome_fantasia": "Updated Name", "cnae": "invalid_cnae"}

    response = client.patch(f"/companies/{company_id}", data=data)

    assert response.status_code == 400


def test_update_company_not_found(client):
    # Test updating a company that doesn't exist
    response = client.patch("/companies/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 500
    assert "Company not found" in response.json["message"]
