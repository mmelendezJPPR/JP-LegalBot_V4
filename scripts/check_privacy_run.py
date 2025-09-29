import sqlite3, os
from pathlib import Path

# Resolve DB path (allow override via CONVERSACIONES_DB or DATABASE_URL)
env_db = os.getenv('CONVERSACIONES_DB') or os.getenv('DATABASE_URL') or 'database/conversaciones.db'
if isinstance(env_db, str) and env_db.startswith('sqlite'):
    if env_db.startswith('sqlite:///'):
        env_db = env_db.replace('sqlite:///', '', 1)
    elif env_db.startswith('sqlite://'):
        env_db = env_db.replace('sqlite://', '', 1)

db_path = Path(env_db)
if not db_path.is_absolute():
    db_path = Path(__file__).resolve().parents[1] / db_path

conn = sqlite3.connect(str(db_path))
conn.row_factory=sqlite3.Row
print('user_consent rows:')
for r in conn.execute("SELECT user_id, memory_consent, consent_at FROM user_consent"):
    print(dict(r))
print('\nlast 10 audit_log:')
for r in conn.execute("SELECT id, user_id, action, details, timestamp FROM audit_log ORDER BY id DESC LIMIT 10"):
    print(dict(r))
conn.close()
