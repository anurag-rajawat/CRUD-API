def test_greet(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to Giganoto!"
