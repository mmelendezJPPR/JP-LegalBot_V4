#!/usr/bin/env python3
"""
Script de verificación final para deployment en Render
Ejecuta todas las pruebas críticas antes del deploy
"""

import os
import sys
import sqlite3
import requests
from pathlib import Path

def check_files():
    """Verificar archivos críticos"""
    required_files = [
        'app.py',
        'Dockerfile',
        'Procfile',
        'requirements.txt',
        'database/conversaciones.db',
        'database/hybrid_knowledge.db',
        'database/Usuarios.db'
    ]

    print('📁 VERIFICANDO ARCHIVOS:')
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f'  ✅ {file}')
        else:
            print(f'  ❌ {file} - FALTANTE')
            all_ok = False
    return all_ok

def check_databases():
    """Verificar bases de datos"""
    print('\n🗄️ VERIFICANDO BASES DE DATOS:')
    all_ok = True

    # Verificar tablas
    dbs = {
        'conversaciones.db': ['conversaciones', 'metricas_rendimiento', 'aprendizaje_sistema'],
        'hybrid_knowledge.db': ['fts_chunks', 'conversation_messages', 'performance_metrics'],
        'Usuarios.db': ['usuarios']
    }

    for db_name, tables in dbs.items():
        db_path = f'database/{db_name}'
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in cur.fetchall()]
            conn.close()

            for table in tables:
                if table in existing_tables:
                    print(f'  ✅ {db_name}:{table}')
                else:
                    print(f'  ❌ {db_name}:{table} - FALTANTE')
                    all_ok = False
        except Exception as e:
            print(f'  ❌ {db_name} - ERROR: {e}')
            all_ok = False

    return all_ok

def check_environment():
    """Verificar variables de entorno críticas"""
    print('\n🔧 VERIFICANDO VARIABLES DE ENTORNO:')

    # En desarrollo local, las variables pueden venir del .env
    # En producción (Render), deben estar configuradas en el dashboard
    from dotenv import load_dotenv
    load_dotenv()

    required_vars = [
        'AZURE_OPENAI_ENDPOINT',
        'AZURE_OPENAI_KEY',
        'AZURE_OPENAI_DEPLOYMENT_NAME',
        'SECRET_KEY'
    ]

    all_ok = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if var == 'AZURE_OPENAI_KEY':
                # Mostrar solo que existe
                print(f'  ✅ {var} (configurado)')
            else:
                print(f'  ✅ {var} = {value}')
        else:
            print(f'  ⚠️  {var} - NO CONFIGURADO (configurar en Render dashboard)')
            # No marcar como error en desarrollo local
            if os.getenv('RENDER'):  # Solo fallar si estamos en Render
                all_ok = False

    return all_ok

def check_imports():
    """Verificar imports críticos"""
    print('\n📦 VERIFICANDO IMPORTS:')
    all_ok = True

    try:
        from ai_system.retrieve import HybridRetriever
        print('  ✅ HybridRetriever importado')
    except Exception as e:
        print(f'  ❌ HybridRetriever error: {e}')
        all_ok = False

    try:
        from ai_system.answer import AnswerEngine
        print('  ✅ AnswerEngine importado')
    except Exception as e:
        print(f'  ❌ AnswerEngine error: {e}')
        all_ok = False

    try:
        from core.auth import login_user
        print('  ✅ Sistema de autenticación importado')
    except Exception as e:
        print(f'  ❌ Sistema de autenticación error: {e}')
        all_ok = False

    return all_ok

def check_app_start():
    """Verificar que la app puede iniciar (simulación)"""
    print('\n🚀 VERIFICANDO INICIO DE APLICACIÓN:')

    try:
        # Simular configuración de producción
        os.environ['FLASK_ENV'] = 'production'
        os.environ['FLASK_DEBUG'] = 'false'

        # Intentar importar la app (sin ejecutarla)
        sys.path.insert(0, '.')
        import app
        print('  ✅ Aplicación importada correctamente')
        return True
    except Exception as e:
        print(f'  ❌ Error importando aplicación: {e}')
        return False

def main():
    """Función principal"""
    print('🔍 VERIFICACIÓN FINAL PARA RENDER DEPLOYMENT')
    print('=' * 60)

    checks = [
        ('Archivos', check_files),
        ('Bases de datos', check_databases),
        ('Variables de entorno', check_environment),
        ('Imports', check_imports),
        ('Inicio de aplicación', check_app_start)
    ]

    results = []
    for name, check_func in checks:
        print(f'\n🔍 Ejecutando verificación: {name}')
        result = check_func()
        results.append((name, result))
        status = '✅ PASÓ' if result else '❌ FALLÓ'
        print(f'📊 Resultado {name}: {status}')

    print('\n' + '=' * 60)
    print('📊 RESUMEN FINAL:')

    all_passed = True
    for name, result in results:
        status = '✅' if result else '❌'
        print(f'  {status} {name}')
        if not result:
            all_passed = False

    print('\n' + '=' * 60)
    if all_passed:
        print('🎉 ¡TODO LISTO PARA RENDER!')
        print('🚀 Puedes proceder con el deployment en render.com')
        print('\n📋 Checklist final:')
        print('  ✅ Repositorio: mmelendezJPPR/JP-LegalBot_V4')
        print('  ✅ Runtime: Docker')
        print('  ✅ Variables de entorno configuradas')
        print('  ✅ Health check: /health')
        print('  ✅ Bases de datos inicializadas')
    else:
        print('❌ HAY PROBLEMAS QUE DEBEN SOLUCIONARSE ANTES DEL DEPLOYMENT')
        print('🔧 Revisa los errores arriba y corrígelos')

    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())