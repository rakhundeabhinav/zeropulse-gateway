import hmac
import hashlib
import json

def generate_signature(secret_key: str, data: dict, timestamp: float) -> str:
    """Generates an HMAC-SHA256 signature for the given payload and timestamp."""
    canonical_str = f"{timestamp}:{json.dumps(data, sort_keys=True)}"
    return hmac.new(
        secret_key.encode("utf-8"),
        canonical_str.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

def verify_signature(secret_key: str, signature: str, data: dict, timestamp: float) -> bool:
    """Verifies that the HMAC signature matches the payload content."""
    expected_sig = generate_signature(secret_key, data, timestamp)
    return hmac.compare_digest(expected_sig, signature)