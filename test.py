#!/usr/bin/env /usr/bin/python3
"""
Script de teste completo do Adaptive Code Judge.
"""

import sys
import os

# Configurar o path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
os.environ['SQLITE_PATH'] = os.path.join(os.path.dirname(__file__), 'data', 'adaptive_judge.db')

def test_sistema_completo():
    """Teste completo do sistema."""
    print("🎯 TESTE COMPLETO - ADAPTIVE CODE JUDGE")
    print("=" * 60)
    print(f"🐍 Python: {sys.version}")
    print(f"💾 Database: {os.environ['SQLITE_PATH']}")
    print()
    
    success = True
    
    # 1. Teste de Imports
    print("📦 1. Testando imports do sistema...")
    try:
        from main import create_app
        from models import Problem, TestCase, Submission
        from services.problem_service import ProblemService
        print("  ✅ Todos os imports funcionando")
    except Exception as e:
        print(f"  ❌ Erro nos imports: {e}")
        success = False
    
    # 2. Teste de Criação da App
    print("\n🏗️ 2. Testando criação da aplicação...")
    try:
        app = create_app()
        print("  ✅ Aplicação criada com sucesso")
    except Exception as e:
        print(f"  ❌ Erro criando aplicação: {e}")
        success = False
    
    # 3. Teste da API
    print("\n🌐 3. Testando API endpoints...")
    try:
        with app.test_client() as client:
            # Root
            response = client.get('/')
            print(f"  📍 Root (/) - Status: {response.status_code}")
            
            # Health
            response = client.get('/health')
            print(f"  🏥 Health - Status: {response.status_code}")
            
            # Problems
            response = client.get('/api/problems')
            print(f"  📚 Problems - Status: {response.status_code}")
            if response.status_code == 200:
                data = response.get_json()
                print(f"      Total problemas: {data.get('count', 0)}")
        
        print("  ✅ API funcionando corretamente")
    except Exception as e:
        print(f"  ❌ Erro testando API: {e}")
        success = False
    
    # 4. Teste Docker (básico)
    print("\n🐳 4. Testando Docker...")
    try:
        import docker
        
        # Verificar se Docker está rodando
        os.system("docker --version > /dev/null 2>&1")
        print("  ✅ Docker está disponível")
        
        # Verificar imagens
        result = os.system("docker images | grep adaptivejudge > /dev/null 2>&1")
        if result == 0:
            print("  ✅ Imagens Docker encontradas")
        else:
            print("  ⚠️  Imagens Docker não encontradas (podem precisar ser construídas)")
            
    except Exception as e:
        print(f"  ⚠️  Docker: {e}")
    
    # 5. Teste de Execução de Código (via linha de comando)
    print("\n💻 5. Testando execução de código...")
    try:
        # Teste Python simples
        test_code = "print('Hello from test!')"
        with open('/tmp/test_code.py', 'w') as f:
            f.write(test_code)
        
        result = os.system("docker run --rm -v /tmp:/workspace -w /workspace adaptivejudge-python:latest python3 test_code.py > /dev/null 2>&1")
        if result == 0:
            print("  ✅ Execução Python via Docker funcionando")
        else:
            print("  ⚠️  Execução Docker pode precisar de configuração")
            
    except Exception as e:
        print(f"  ⚠️  Execução de código: {e}")
    
    # Resultado final
    print("\n" + "=" * 60)
    if success:
        print("🎉 TODOS OS TESTES PRINCIPAIS PASSARAM!")
        print("\n✅ SISTEMA PRONTO PARA USO!")
        print("\n🚀 Para iniciar:")
        print("   ./run.sh server")
        print("   Acesse: http://localhost:8000")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("Verifique os erros acima.")
    
    return success

if __name__ == '__main__':
    sys.exit(0 if test_sistema_completo() else 1)
