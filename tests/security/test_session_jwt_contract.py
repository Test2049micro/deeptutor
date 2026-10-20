"""Exercise session-token policy with real HS256 signatures, including legacy tokens."""

import base64
import hashlib
import hmac
import json
import time

import pytest

from deeptutor.services import auth

SECRET = "isolated-session-regression-secret-never-used-outside-tests"


def _signed_token(claims, secret=SECRET):
    def segment(value):
        return base64.urlsafe_b64encode(json.dumps(value).encode()).rstrip(b"=")

    unsigned = b".".join([segment({"alg": "HS256", "typ": "JWT"}), segment(claims)])
    signature = base64.urlsafe_b64encode(
        hmac.digest(secret.encode(), unsigned, hashlib.sha256)
    ).rstrip(b"=")
    return b".".join([unsigned, signature]).decode()


@pytest.fixture(autouse=True)
def isolated_session_secret(monkeypatch):
    monkeypatch.setattr(auth, "AUTH_SECRET", SECRET)
    monkeypatch.setattr(auth, "POCKETBASE_ENABLED", False)


def _claims():
    now = int(time.time())
    return {
        "sub": "legacy-user",
        "uid": "user-123",
        "role": "user",
        "iat": now,
        "exp": now + 300,
    }


def test_signed_session_without_expiry_is_rejected():
    claims = _claims()
    del claims["exp"]
    assert auth.decode_token(_signed_token(claims)) is None


def test_existing_hs256_token_remains_compatible():
    result = auth.decode_token(_signed_token(_claims()))
    assert result is not None
    assert result.username == "legacy-user"
    assert result.user_id == "user-123"
    assert result.role == "user"


def test_newly_issued_token_round_trips():
    result = auth.decode_token(auth.create_token("new-user", user_id="user-456"))
    assert result is not None
    assert result.username == "new-user"
    assert result.user_id == "user-456"


def test_wrong_signature_is_rejected():
    assert auth.decode_token(_signed_token(_claims(), secret="wrong-secret")) is None


def test_expired_session_is_rejected():
    claims = _claims()
    claims["exp"] = int(time.time()) - 60
    assert auth.decode_token(_signed_token(claims)) is None
