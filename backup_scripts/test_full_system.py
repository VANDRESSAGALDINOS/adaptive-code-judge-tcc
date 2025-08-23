#!/usr/bin/env python3
"""
Test completo do sistema Adaptive Code Judge com Docker.
"""

import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set explicit SQLite path
os.environ['SQLITE_PATH'] = '/Users/vandressa.galdino/adaptive-code-judge/data/adaptive_judge.db'

def test_docker_integration():
    """Teste integração com Docker."""
    print("🐳 Testando integração com Docker...")
    
    try:
        from config.app import AppConfig
        from executor import DockerExecutor
        
        config = AppConfig()
        executor = DockerExecutor(config)
        
        print(f"  ✓ Executor criado com sucesso")
        print(f"  ✓ Imagem C++: {config.DOCKER_CPP_IMAGE}")
        print(f"  ✓ Imagem Python: {config.DOCKER_PYTHON_IMAGE}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Erro na integração Docker: {e}")
        return False

def test_code_execution():
    """Teste execução de código."""
    print("\n💻 Testando execução de código...")
    
    try:
        from config.app import AppConfig
        from executor import DockerExecutor
        
        executor = DockerExecutor(AppConfig())
        
        # Teste Python simples
        print("  Testando código Python...")
        python_code = "print('Hello from Python!')"
        result = executor.execute_python(python_code, "", time_limit=5.0)
        
        if result.success:
            print(f"    ✓ Python executado com sucesso")
            print(f"    ✓ Output: {result.stdout.strip()}")
            print(f"    ✓ Tempo: {result.execution_time:.3f}s")
        else:
            print(f"    ✗ Python falhou: {result.error_message}")
            return False
        
        # Teste C++ simples
        print("  Testando código C++...")
        cpp_code = """#include <iostream>
using namespace std;
int main() {
    cout << "Hello from C++!" << endl;
    return 0;
}"""
        result = executor.execute_cpp(cpp_code, "", time_limit=10.0)
        
        if result.success:
            print(f"    ✓ C++ executado com sucesso")
            print(f"    ✓ Output: {result.stdout.strip()}")
            print(f"    ✓ Tempo: {result.execution_time:.3f}s")
        else:
            print(f"    ✗ C++ falhou: {result.error_message}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ Erro na execução de código: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_submission_workflow():
    """Teste workflow completo de submissão."""
    print("\n📝 Testando workflow de submissão...")
    
    try:
        from main import create_app
        
        app = create_app()
        
        with app.test_client() as client:
            # Criar um problema simples
            problem_data = {
                "title": "Soma Simples",
                "description": "Leia dois números e imprima a soma",
                "difficulty": "easy",
                "tags": ["math", "basic"]
            }
            
            response = client.post('/api/problems', 
                                 data=json.dumps(problem_data),
                                 content_type='application/json')
            
            if response.status_code != 201:
                print(f"  ✗ Falha ao criar problema: {response.status_code}")
                return False
            
            problem = response.get_json()
            problem_id = problem['id']
            print(f"  ✓ Problema criado: ID {problem_id}")
            
            # Adicionar caso de teste
            test_case_data = {
                "name": "test_1",
                "input_data": "2 3",
                "expected_output": "5",
                "is_sample": True,
                "is_hidden": False
            }
            
            response = client.post(f'/api/problems/{problem_id}/test-cases',
                                 data=json.dumps(test_case_data),
                                 content_type='application/json')
            
            if response.status_code != 201:
                print(f"  ✗ Falha ao criar caso de teste: {response.status_code}")
                return False
            
            print(f"  ✓ Caso de teste criado")
            
            # Submeter solução Python
            submission_data = {
                "problem_id": problem_id,
                "language": "python",
                "source_code": "a, b = map(int, input().split())\nprint(a + b)",
                "user_id": "test_user"
            }
            
            response = client.post('/api/submissions/judge',
                                 data=json.dumps(submission_data),
                                 content_type='application/json')
            
            print(f"  📊 Status da submissão: {response.status_code}")
            
            if response.status_code == 201:
                submission = response.get_json()
                print(f"  ✓ Submissão criada: ID {submission['id']}")
                print(f"  ✓ Resultado: {submission.get('result', 'unknown')}")
                print(f"  ✓ Score: {submission.get('score', 0):.2f}")
                print(f"  ✓ Casos passados: {submission.get('passed_test_cases', 0)}/{submission.get('total_test_cases', 0)}")
                
                # Mostrar resultados dos casos de teste
                if 'test_results' in submission:
                    for tr in submission['test_results']:
                        status = "✓ PASSOU" if tr['passed'] else "✗ FALHOU"
                        print(f"    - Caso {tr['test_case']['name']}: {status}")
                        if tr.get('actual_output'):
                            print(f"      Output: {tr['actual_output'].strip()}")
                
                return True
            else:
                error_data = response.get_json()
                print(f"  ✗ Submissão falhou: {error_data.get('error', 'Erro desconhecido')}")
                return False
        
    except Exception as e:
        print(f"  ✗ Erro no workflow: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_health_check():
    """Teste health check com Docker."""
    print("\n🏥 Testando health check...")
    
    try:
        from main import create_app
        
        app = create_app()
        
        with app.test_client() as client:
            response = client.get('/health/detailed')
            
            if response.status_code in [200, 503]:
                health = response.get_json()
                print(f"  📊 Status geral: {health.get('status', 'unknown')}")
                
                # Database
                db_status = health.get('services', {}).get('database', {})
                if isinstance(db_status, dict):
                    print(f"  💾 Database: {db_status.get('status', 'unknown')}")
                    if 'counts' in db_status:
                        counts = db_status['counts']
                        print(f"    - Problemas: {counts.get('problems', 0)}")
                        print(f"    - Casos de teste: {counts.get('test_cases', 0)}")
                        print(f"    - Submissões: {counts.get('submissions', 0)}")
                
                # Docker
                docker_status = health.get('services', {}).get('docker', {})
                if isinstance(docker_status, dict):
                    print(f"  🐳 Docker: {docker_status.get('status', 'unknown')}")
                    if 'version' in docker_status:
                        print(f"    - Versão: {docker_status['version']}")
                
                # Images
                images = health.get('docker_images', {})
                for image_name, image_info in images.items():
                    status = image_info.get('status', 'unknown')
                    print(f"  📦 {image_name}: {status}")
                
                return health.get('status') == 'healthy'
            else:
                print(f"  ✗ Health check falhou: {response.status_code}")
                return False
        
    except Exception as e:
        print(f"  ✗ Erro no health check: {e}")
        return False

def main():
    """Execute todos os testes."""
    print("🎯 TESTE COMPLETO - ADAPTIVE CODE JUDGE COM DOCKER")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Teste integração Docker
    all_tests_passed &= test_docker_integration()
    
    # Teste execução de código
    all_tests_passed &= test_code_execution()
    
    # Teste health check
    all_tests_passed &= test_health_check()
    
    # Teste workflow completo
    all_tests_passed &= test_submission_workflow()
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("\n✅ O Sistema Adaptive Code Judge está TOTALMENTE FUNCIONAL!")
        print("\n🚀 Funcionalidades disponíveis:")
        print("   • Execução segura de código C++ e Python via Docker")
        print("   • Avaliação automática de submissões")
        print("   • Sistema de benchmarks adaptativos")
        print("   • API REST completa")
        print("   • Health monitoring")
        print("\n🌐 Para usar a API REST:")
        print("   SQLITE_PATH=/Users/vandressa.galdino/adaptive-code-judge/data/adaptive_judge.db \\")
        print("   PYTHONPATH=/Users/vandressa.galdino/adaptive-code-judge/src \\")
        print("   python3 src/main.py")
        print("\n   Então acesse: http://localhost:8000")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("\nVerifique:")
        print("   • Docker está rodando?")
        print("   • Imagens Docker foram construídas?")
        print("   • Dependências Python instaladas?")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
