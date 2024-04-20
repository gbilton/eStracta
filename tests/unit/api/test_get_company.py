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


def test_get_company_existing(client, db):
    # Test getting an existing company
    company_id = create_test_company()

    response = client.get(f"/companies/{company_id}")

    assert response.status_code == 200
    assert response.json["id"] == str(company_id)


def test_get_company_not_found(client):
    # Test getting a company that doesn't exist
    response = client.get("/companies/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 500
    assert "Company not found" in response.json["message"]


def test_get_company_invalid_id(client):
    # Test getting a company with an invalid ID
    response = client.get("/companies/invalid_id")

    assert response.status_code == 404
