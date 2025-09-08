from nacl import public
import base64
import requests
import os
import json

GITHUB_REPO = "cgalatro2/summail"
GITHUB_SECRET_NAME = "TOKEN_JSON_B64"
GITHUB_PAT = os.environ["GH_PAT"]


def update_token_secret(token_json_str: str):
    print("🔐 Uploading new token.json to GitHub secret...")

    # Base64 encode the string directly
    encoded = base64.b64encode(token_json_str.encode("utf-8")).decode("utf-8")

    # Get public key
    headers = {"Authorization": f"Bearer {GITHUB_PAT}"}
    res = requests.get(
        f"https://api.github.com/repos/{GITHUB_REPO}/actions/secrets/public-key",
        headers=headers,
    )
    res.raise_for_status()
    key_data = res.json()

    # Encrypt secret with public key
    public_key_bytes = base64.b64decode(key_data["key"])
    sealed_box = public.SealedBox(public.PublicKey(public_key_bytes))
    encrypted = sealed_box.encrypt(encoded.encode("utf-8"))
    encrypted_value = base64.b64encode(encrypted).decode("utf-8")

    # Upload secret
    res = requests.put(
        f"https://api.github.com/repos/{GITHUB_REPO}/actions/secrets/{GITHUB_SECRET_NAME}",
        headers={
            "Authorization": f"Bearer {GITHUB_PAT}",
            "Content-Type": "application/json",
        },
        json={
            "encrypted_value": encrypted_value,
            "key_id": key_data["key_id"],
        },
    )
    res.raise_for_status()
    print("✅ GitHub secret TOKEN_JSON_B64 updated.")
