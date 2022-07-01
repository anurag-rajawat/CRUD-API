def test_greet(dummy_client):
    response = dummy_client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to Giganoto!"
