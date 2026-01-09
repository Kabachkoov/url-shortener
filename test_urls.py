def test_create_short_url(client, test_user):
    # Login
    login_response = client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create short URL
    url_data = {
        "original_url": "https://example.com",
        "custom_code": "test123"
    }
    
    response = client.post("/api/v1/urls/", json=url_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["short_code"] == "test123"
    assert data["original_url"] == "https://example.com"


def test_get_user_urls(client, test_user):
    # Login
    login_response = client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get user URLs
    response = client.get("/api/v1/urls/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
