from app.models.users import User


def test_user_creation(db):
    user = User(
        username="test_user",
        email="test@example.com",
        password_hash="fake_hash"
    )

    db.add(user)
    db.commit()

    saved_user = db.query(User).filter_by(
        username="test_user"
    ).first()

    assert saved_user is not None

def test_user_does_not_exist(db):
    user = db.query(User).filter_by(
        username="test_user"
    ).first()

    assert user is None