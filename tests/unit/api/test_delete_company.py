from unittest.mock import patch
from app.models.company import Company


@patch("app.main.delete_company")
def test_delete_existing_company(mock_delete_company, client, db):
    # Create a test company to delete
    test_company = Company(
        cnpj="12345678901234",
        nome_razao="Test Company",
        nome_fantasia="Test",
        cnae="1234567",
    )
    db.session.add(test_company)
    db.session.commit()

    # Mock the delete_company function to return a successful deletion
    mock_delete_company.return_value = None

    # Send a DELETE request to delete the test company
    response = client.delete("/companies/12345678901234")

    # Check that the company is deleted and response status is 204
    assert response.status_code == 204
    assert (
        db.session.query(Company).filter_by(cnpj="12345678901234").count() == 0
    )


@patch("app.routes.delete_company")
def test_delete_non_existing_company(mock_delete_company, client, db):
    # Mock the delete_company function to return a failure for deleting a non-existing company
    mock_delete_company.side_effect = Exception("Company not found")

    # Send a DELETE request to delete a non-existing company
    response = client.delete("/companies/99999999999999")

    # Check that the response status is 404
    assert response.status_code == 404


@patch("app.routes.delete_company")
def test_delete_company_invalid_cnpj(mock_delete_company, client):
    # Mock the delete_company function to simulate an invalid CNPJ format
    mock_delete_company.side_effect = Exception("Invalid CNPJ format")

    # Send a DELETE request with an invalid CNPJ format
    response = client.delete("/companies/invalid_cnpj")

    # Check that the response status is 400
    assert response.status_code == 400
