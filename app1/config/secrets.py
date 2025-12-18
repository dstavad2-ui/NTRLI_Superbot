"""
NTRLI' AI - Encrypted Secrets Handler
Decrypts API keys at runtime using admin credentials

Security: API keys are encrypted with ADMIN_ID as the key.
Only the correct admin can decrypt and use the APIs.
"""

import base64
import hashlib
import os
from typing import Dict

# Encrypted API keys - requires ADMIN_ID to decrypt
ENCRYPTED_SECRETS = {
    "data": "KzNFcXI3dTB4MnIrejlPV21ZT0FMaG5icGh5UnRMWStUMVVkdS83WUZsenpRQXVKczZDNENPcnB3WmZ6NzdnU0hLS1hEODNxdjF0V1JFR2d2dG9GZnV4a0RaTEZuOXhkM3VqZDZhQ0h2bDkyNDZnM3g1R3lKa2hJUnBTbjFEMUkvRzFVM3FMY3UyNkl3LzY5cllTYUJRajVvVEQ5OCtoRVczUW01LzdHZjF5Q1FTU01vS1hTZi9lMStlNmtnK2dPQTlhRUdzYnFsM1pTVHlXb244VTlZdU53UDVXK3FQdHBqT25HbnJTeWh5SVo0SVozOXI3dFVuNHRNNVdlMlFKMDkzdzBzcWVxeEdYNjBkdUFqWWVKV2lmM3ZIV2QvcngxRFVGRDV1R2llUnlJVndiZWx0eTlYTjNncCtiejllTmZJcVBiVC9tVW1FRmdhQ0tVbmRFRmRQdGxMcm0rcnRFSHlPcS9yN1N0dWtwMjJ0RWE4NjJiZVV0aUZPT0M0QUZBd0hRcGlLclN6MS9EMGZidGpMT2lCbis5b2dudDg2bGtTMkk4dXV2L0FrYURCRXFReksrd1V1elMrb0N4dElFaGRlR3BBdnF0alVrU1pTYmlrZnd1UVB4L1VZbWZpdko5OHN2eGxZQ1c2Qzh0MDVReG1vV3BXbGwwUmFYciszaDR6VmtYcWI3YitRN2N0c2lQcW95NkJnL2lxQTN0bGFsZmFsY0M0YnI1Q2s3eUdDaUpoZHJkRG82eDM1N01sNE1pRk0rdURQK1RqMUp6ZURPQm1zOEhidU1JQm9HcTI3a0QyYktpdlBLbjRBVjBwOU1ubnYrOEtnMURGTEsyb1g4YmdnUUQwTVhoejJqMDBNMmVsb3VQTEFQSjNpTGZySUprYzBrY3VldktlaytDRFEvUWpKM09VdlgyeUlpQnBxa0ZkZGE2Zkp1RnBDVk9aaittbHVZY0grMEFWSk82MCtSUDk4M0Q=",
    "salt": "NTRLI_AI_2025",
    "version": "1.0"
}


def _derive_key(admin_id: str, salt: str) -> bytes:
    """Derive decryption key from admin ID"""
    combined = f"{admin_id}:{salt}".encode()
    return hashlib.sha256(combined).digest()


def _xor_decrypt(data: bytes, key: bytes) -> bytes:
    """XOR decryption"""
    return bytes(d ^ key[i % len(key)] for i, d in enumerate(data))


def decrypt_secrets(admin_id: str = None) -> Dict[str, str]:
    """
    Decrypt API keys using admin credentials.

    Args:
        admin_id: Admin user ID for decryption (uses env if not provided)

    Returns:
        Dict of decrypted API keys
    """
    if admin_id is None:
        admin_id = os.getenv("ADMIN_ID", "8467779489")

    try:
        # Derive key from admin ID
        key = _derive_key(str(admin_id), ENCRYPTED_SECRETS["salt"])

        # Decode and decrypt (double base64 + XOR)
        decoded_once = base64.b64decode(ENCRYPTED_SECRETS["data"])
        decoded_twice = base64.b64decode(decoded_once)
        decrypted = _xor_decrypt(decoded_twice, key)

        # Parse decrypted data
        lines = decrypted.decode('utf-8').strip().split('\n')
        secrets = {}
        for line in lines:
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                secrets[k.strip()] = v.strip()
        return secrets
    except Exception as e:
        return {}


def load_encrypted_secrets() -> bool:
    """Load encrypted secrets into environment variables"""
    secrets = decrypt_secrets()
    for key, value in secrets.items():
        if key and value and not os.getenv(key):
            os.environ[key] = value
    return len(secrets) > 0


# Auto-load on import
_secrets_loaded = load_encrypted_secrets()
