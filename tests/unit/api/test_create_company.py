def test_create_company_valid_data(client):
    data = {
        "cnpj": "00623904000173",
        "nome_razao": "Company ABC",
        "nome_fantasia": "ABC",
        "cnae": "1234567",
    }

    response = client.post("/companies", data=data)

    assert response.status_code == 201
    assert response.json["cnpj"] == data["cnpj"]
    assert response.json["nome_razao"] == data["nome_razao"]
    assert response.json["nome_fantasia"] == data["nome_fantasia"]
    assert response.json["cnae"] == data["cnae"]


def test_create_company_invalid_cnpj(client):
    data = {
        "cnpj": "invalid",
        "nome_razao": "Company ABC",
        "nome_fantasia": "ABC",
        "cnae": "1234567",
    }

    response = client.post("/companies", data=data)

    assert response.status_code == 400
    assert "Invalid Parameters." in response.json["error"]


def test_create_company_invalid_cnae(client):
    data = {
        "cnpj": "12345678901234",
        "nome_razao": "Company ABC",
        "nome_fantasia": "ABC",
        "cnae": "invalid",
    }

    response = client.post("/companies", data=data)

    assert response.status_code == 400
    assert "Invalid Parameters." in response.json["error"]


def test_create_company_missing_fields(client):
    data = {
        "cnpj": "12345678901234",
        "nome_fantasia": "ABC",
        # Missing "nome_razao" and "cnae" fields
    }

    response = client.post("/companies", data=data)

    assert response.status_code == 400
