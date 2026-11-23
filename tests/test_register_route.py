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

    assert data["user"]["username"] == "testuser"
    assert data["user"]["email"] == "test@mail.com"

    assert "password" not in data
    assert "password_hash" not in data

def test_register_incorrect_data(client):
    response = client.post(
        "/users/register",
        json={
            "username": "1",
            "email" : "testmail.com",
            "password" : "11"
        }
    )

    print(response.json())
    assert response.status_code == 422

def test_register_conflict(client):
    response1 = client.post(
        "/users/register",
        json={
            "username" : "testuser",
            "email" : "test@mail.com",
            "password" : "1111"
        }
    )
    response2 = client.post(
        "/users/register",
        json={
            "username" : "testuser",
            "email" : "test@mail.com",
            "password" : "1111"
        }
    )

    assert response2.status_code == 409

def test_register_conflict_email(client):
    response1 = client.post(
        "/users/register",
        json={
            "username" : "testuser",
            "email" : "test@mail.com",
            "password" : "1111"
        }
    )
    response2 = client.post(
        "/users/register",
        json={
            "username" : "anothertestuser",
            "email" : "test@mail.com",
            "password" : "1111"
        }
    )
    assert response1.status_code == 201
    
    assert response2.status_code == 409
