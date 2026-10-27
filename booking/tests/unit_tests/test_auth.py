from src.services.auth import AuthService


def test_create_access_token():
    jwt_token = AuthService().create_access_token(data={'user_id': 1})
    assert isinstance(jwt_token, str)


def test_decode_token():
    jwt_token = AuthService().create_access_token(data={'user_id': 1})
    decoded_token = AuthService().decode_token(token=jwt_token)
    assert decoded_token['user_id'] == 1
