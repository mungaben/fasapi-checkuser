# app/utils/csrf.py
import hmac
import hashlib
import time
from fastapi import HTTPException

CSRF_SECRET = b'supersecretcsrfkey'

# Generate CSRF token (HMAC-based)
def generate_csrf_token():
    timestamp = str(int(time.time())).encode('utf-8')
    token = hmac.new(CSRF_SECRET, timestamp, hashlib.sha256).hexdigest()
    return f"{token}:{timestamp.decode('utf-8')}"

# Validate CSRF token
def validate_csrf_token(token: str):
    try:
        token, timestamp = token.split(":")
        expected_token = hmac.new(CSRF_SECRET, timestamp.encode('utf-8'), hashlib.sha256).hexdigest()
        
        # Token expires after 1 hour
        if time.time() - int(timestamp) > 3600:
            raise HTTPException(status_code=403, detail="CSRF token expired")
        
        if not hmac.compare_digest(expected_token, token):
            raise HTTPException(status_code=403, detail="Invalid CSRF token")
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
