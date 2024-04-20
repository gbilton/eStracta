import json


def test_sequence(client):
    # Step 1: Add two companies
    company_data_1 = {
        "cnpj": "12345678901234",
        "nome_razao": "Company A",
        "nome_fantasia": "A",
        "cnae": "1234567",
    }
    response = client.post("/companies", data=company_data_1)
    assert response.status_code == 201
    company_id_1 = json.loads(response.data)["id"]

    company_data_2 = {
        "cnpj": "23456789012345",
        "nome_razao": "Company B",
        "nome_fantasia": "B",
        "cnae": "2345678",
    }
    response = client.post("/companies", data=company_data_2)
    assert response.status_code == 201
    company_id_2 = json.loads(response.data)["id"]

    # Step 2: Get all companies
    response = client.get("/companies")
    assert response.status_code == 200
    assert len(response.json) == 2  # Assuming two companies were created

    # Step 3: Get one company
    response = client.get(f"/companies/{company_id_1}")
    assert response.status_code == 200
    assert response.json["id"] == company_id_1

    # Step 4: Update one company
    update_data = {"nome_fantasia": "Updated Name", "cnae": "8765432"}
    response = client.patch(f"/companies/{company_id_1}", data=update_data)
    assert response.status_code == 200
    assert response.json["nome_fantasia"] == "Updated Name"
    assert response.json["cnae"] == "8765432"

    # Step 5: Delete one company
    response = client.delete(f"/companies/{company_id_2}")
    assert response.status_code == 204
