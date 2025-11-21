from app.core.security import hash_password, verify_password

def test_password_hashing():
    senha_plana = "minhasenha123"

    hashed = hash_password(senha_plana)

    assert hashed != senha_plana
    assert verify_password(senha_plana, hashed) is True
    assert verify_password("senhaerrada", hashed) is False