"""
OmniScope OSINT: Secure SQLite 3 Key and Credentials Vault
Stores all API tokens, access credentials, and keys securely in an obfuscated SQLite 3 database.
Zero plaintext in code or cached JSON files.
"""

import os
import sqlite3
import base64
import time
from typing import Dict, Optional, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT_DB_PATH = os.path.join(BASE_DIR, "data", "vault.db")

_VAULT_SALT = b"OMNISCOPE_OSINT_SECURE_VAULT_2026_K9X"

def _encode_val(raw_val: str) -> str:
    if not raw_val:
        return ""
    data = raw_val.encode("utf-8")
    salt_len = len(_VAULT_SALT)
    scrambled = bytearray(b ^ _VAULT_SALT[i % salt_len] for i, b in enumerate(data))
    return base64.b85encode(scrambled).decode("ascii")

def _decode_val(enc_val: str) -> str:
    if not enc_val:
        return ""
    try:
        scrambled = base64.b85decode(enc_val.encode("ascii"))
        salt_len = len(_VAULT_SALT)
        data = bytearray(b ^ _VAULT_SALT[i % salt_len] for i, b in enumerate(scrambled))
        return data.decode("utf-8")
    except Exception:
        return enc_val

def _get_conn() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(VAULT_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(VAULT_DB_PATH, timeout=20.0)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS api_vault (
            key_name TEXT PRIMARY KEY,
            key_value TEXT NOT NULL,
            description TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    return conn

def get_vault_key(key_name: str, default: str = "") -> str:
    try:
        conn = _get_conn()
        cur = conn.cursor()
        cur.execute("SELECT key_value FROM api_vault WHERE key_name = ?;", (key_name.strip(),))
        row = cur.fetchone()
        conn.close()
        if row and row[0]:
            return _decode_val(row[0])
    except Exception:
        pass
    return default

def set_vault_key(key_name: str, key_value: str, description: str = ""):
    conn = _get_conn()
    cur = conn.cursor()
    enc_val = _encode_val(key_value.strip())
    cur.execute('''
        INSERT INTO api_vault (key_name, key_value, description, updated_at)
        VALUES (?, ?, ?, datetime('now'))
        ON CONFLICT(key_name) DO UPDATE SET
            key_value = excluded.key_value,
            description = excluded.description,
            updated_at = excluded.updated_at;
    ''', (key_name.strip(), enc_val, description))
    conn.commit()
    conn.close()

def get_all_vault_keys() -> Dict[str, str]:
    res = {}
    try:
        conn = _get_conn()
        cur = conn.cursor()
        cur.execute("SELECT key_name, key_value FROM api_vault;")
        rows = cur.fetchall()
        conn.close()
        for k, v in rows:
            res[k] = _decode_val(v)
    except Exception:
        pass
    return res

def delete_vault_key(key_name: str):
    conn = _get_conn()
    conn.execute("DELETE FROM api_vault WHERE key_name = ?;", (key_name.strip(),))
    conn.commit()
    conn.close()
