def test_api_health(client):
    response = client.get("/")
    assert b"ok" in response.data
