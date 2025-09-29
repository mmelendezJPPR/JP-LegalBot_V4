#!/usr/bin/env python3
"""
Script para inicializar las tablas faltantes en hybrid_knowledge.db
"""

import sqlite3
import os
from pathlib import Path

def init_hybrid_knowledge_db():
    """Inicializa las tablas faltantes en hybrid_knowledge.db"""

    # Crear directorio database si no existe
    db_dir = Path('database')
    db_dir.mkdir(exist_ok=True)

    # Ruta de la base de datos de aprendizaje
    db_path = db_dir / 'hybrid_knowledge.db'

    print(f'🔧 Inicializando hybrid_knowledge.db en: {db_path}')

    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Crear tabla de conversaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                specialist_type TEXT,
                session_id TEXT,
                started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                ended_at DATETIME,
                status TEXT DEFAULT 'active'
            )
        ''')

        # Crear tabla de mensajes de conversación
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_messages (
                id TEXT PRIMARY KEY,
                conversation_id TEXT,
                role TEXT,
                content TEXT,
                specialist_context TEXT,
                processing_time REAL,
                confidence_score REAL,
                sources_used TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
        ''')

        # Crear tabla de métricas de rendimiento
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id TEXT PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                metric_type TEXT,
                metric_value REAL,
                specialist_area TEXT,
                context_data TEXT
            )
        ''')

        # Crear tabla FTS para búsqueda de texto completo
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS fts_chunks USING fts5(
                id, content, doc_id, heading_path, page_start, page_end
            )
        ''')

        # Crear índices para mejor rendimiento
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_session ON conversations(session_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_conversation ON conversation_messages(conversation_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON conversation_messages(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON performance_metrics(timestamp)')

        # Confirmar cambios
        conn.commit()

        # Verificar que las tablas se crearon correctamente
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = cursor.fetchall()

        print('✅ Base de datos hybrid_knowledge.db inicializada correctamente')
        print(f'📊 Tablas creadas: {[tabla[0] for tabla in tablas]}')

        conn.close()

    except Exception as e:
        print(f'❌ Error inicializando base de datos: {e}')
        raise

if __name__ == '__main__':
    init_hybrid_knowledge_db()