#!/usr/bin/env python3
"""
Teste simples para verificar se tudo está funcionando.
"""

import sys
import os

# Configurar o path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configurar variáveis de ambiente
os.environ['SQLITE_PATH'] = os.path.join(os.path.dirname(__file__), 'data', 'adaptive_judge.db')

def test_imports():
    """Teste básico de imports."""
    print("🔍 Testando imports...")
    
    try:
        print("  📦 Testando config...")
        from config.app import AppConfig
        print("  ✅ Config OK")
        
        print("  📦 Testando models...")
        from models import db, Problem, TestCase
        print("  ✅ Models OK")
        
        print("  📦 Testando services...")
        from services.problem_service import ProblemService
        print("  ✅ Services OK")
        
        print("  📦 Testando API...")
        from api.health import health_bp
        print("  ✅ API OK")
        
        print("  📦 Testando main...")
        from main import create_app
        print("  ✅ Main OK")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erro no import: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app_creation():
    """Teste criação da aplicação."""
    print("\n🏗️ Testando criação da aplicação...")
    
    try:
        from main import create_app
        
        app = create_app()
        print("  ✅ Aplicação criada com sucesso!")
        
        # Teste básico da aplicação
        with app.test_client() as client:
            response = client.get('/')
            print(f"  📊 Status root endpoint: {response.status_code}")
            
            response = client.get('/health')
            print(f"  📊 Status health endpoint: {response.status_code}")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Erro criando aplicação: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Executar testes."""
    print("🎯 TESTE DIAGNÓSTICO - ADAPTIVE CODE JUDGE")
    print("=" * 50)
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Diretório: {os.path.dirname(__file__)}")
    print(f"💾 Database: {os.environ.get('SQLITE_PATH')}")
    print()
    
    success = True
    
    # Teste imports
    success &= test_imports()
    
    # Teste criação da app
    if success:
        success &= test_app_creation()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("\n✅ O sistema está funcionando corretamente!")
        print("\n🚀 Para iniciar o servidor:")
        print("   python3 start_server.py")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("\nVerifique os erros acima.")
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
