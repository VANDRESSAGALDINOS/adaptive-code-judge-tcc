#!/usr/bin/env /usr/bin/python3
"""
Script simples para iniciar o Adaptive Code Judge.
"""

import sys
import os

# Configurar o path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configurar variáveis de ambiente
os.environ['SQLITE_PATH'] = os.path.join(os.path.dirname(__file__), 'data', 'adaptive_judge.db')

if __name__ == '__main__':
    print("🚀 Iniciando Adaptive Code Judge...")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Diretório: {os.path.dirname(__file__)}")
    print(f"💾 Database: {os.environ['SQLITE_PATH']}")
    print()
    
    try:
        # Importar e executar
        from main import create_app
        
        app = create_app()
        
        print("✅ Aplicação criada com sucesso!")
        print("🌐 Iniciando servidor em http://localhost:8000")
        print("Press Ctrl+C to stop")
        print("-" * 50)
        
        app.run(
            host='0.0.0.0',
            port=8000,
            debug=True,
            threaded=True
        )
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
