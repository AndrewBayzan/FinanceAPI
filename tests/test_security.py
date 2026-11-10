from app.core.security import hash_password, verify_password



def test_hash_password():
    password = "qwerty123"
    hashed = hash_password(password)
    assert hashed != password

def test_verify_password_correct():
    password = "qwerty123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True

def test_password_salt():
    password = "qwerty123"
    hashed = hash_password(password)
    password2 = "qwerty123"

    hashed2 = hash_password(password2)

    assert hashed != hashed2

def test_verify_password_incorrect():
    password = "qwerty123"
    incorrect_password = "zxcvb123"

    hashed = hash_password(password)

    assert verify_password(incorrect_password, hashed) is False