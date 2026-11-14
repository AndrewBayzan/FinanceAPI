import pytest


def test_register_user(client):
    response = client.post(
        "/users/register",
        json={
            "username" : "testuser",
            "email" : "test@mail.com",
            "password" : "1111"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@mail.com"

    assert "password" not in data
    assert "password_hash" not in data
