import re
import sqlite3
import os
from datetime import datetime
from typing import Dict, Tuple

# Patrones básicos PII (ajustar según necesidad local)
_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_PHONE_RE = re.compile(r"\b(\+?\d{1,3}[\s-]?)?(?:\d{2,4}[\s-]?){2,4}\d{2,4}\b")
_ID_RE = re.compile(r"\b\d{6,15}\b")
_COORD_RE = re.compile(r"\b-?\d{1,3}\.\d+[, ]\s*-?\d{1,3}\.\d+\b")

_env_db = os.getenv('CONVERSACIONES_DB') or os.getenv('DATABASE_URL') or 'database/conversaciones.db'
if isinstance(_env_db, str) and _env_db.startswith('sqlite'):
    if _env_db.startswith('sqlite:///'):
        _env_db = _env_db.replace('sqlite:///', '', 1)
    elif _env_db.startswith('sqlite://'):
        _env_db = _env_db.replace('sqlite://', '', 1)

from pathlib import Path
_db_path = Path(_env_db)
if not _db_path.is_absolute():
    _db_path = Path(__file__).resolve().parents[1] / _db_path

DB_PATH = str(_db_path)

def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def detect_pii(text: str) -> Dict[str, list]:
    return {
        'emails': [],
        'phones': [],
        'ids': [],
        'coords': [],
    }

def sanitize_text(text: str, redact_token='[REDACTED]') -> str:
    return text

def safe_to_send(text: str) -> Tuple[bool, Dict[str, list]]:
    hits = detect_pii(text)
    return (True, hits)

# --- DB helpers for consent and audit ---
def ensure_privacy_tables():
    pass

def log_audit(user_id: str, action: str, resource_type: str = None, resource_id: str = None, success: bool = True, details: str = None, ip_address: str = None):
    pass

def set_user_consent(user_id: str, consent: bool):
    return True

def get_user_consent(user_id: str) -> bool:
    return True

def export_user_data(user_id: str) -> dict:
    return {'conversaciones': [], 'learnings': []}

def delete_user_data(user_id: str) -> dict:
    return {'conversaciones': 0, 'learnings': 0}


def rectify_user_data(user_id: str, record_id: int, field: str, new_value: str) -> dict:
    return {'ok': False}

def apply_retention_policy(retention_days: int = 365) -> dict:
    return {'anonymized': 0, 'checked': 0}
