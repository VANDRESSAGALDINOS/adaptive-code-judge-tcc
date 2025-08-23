#!/usr/bin/env python3
"""
Teste simples do Docker para verificar se as imagens funcionam.
"""

import docker
import tempfile
import os

def test_docker_connection():
    """Teste conexão com Docker."""
    print("🐳 Testando conexão com Docker...")
    
    try:
        client = docker.from_env()
        client.ping()
        version = client.version()
        print(f"  ✓ Docker conectado - versão {version['Version']}")
        return client
    except Exception as e:
        print(f"  ✗ Erro conectando Docker: {e}")
        return None

def test_cpp_image(client):
    """Teste da imagem C++."""
    print("\n🔧 Testando imagem C++...")
    
    try:
        # Verificar se a imagem existe
        try:
            image = client.images.get('adaptivejudge-cpp:latest')
            print(f"  ✓ Imagem encontrada: {image.short_id}")
        except docker.errors.ImageNotFound:
            print("  ✗ Imagem adaptivejudge-cpp:latest não encontrada")
            return False
        
        # Código C++ simples
        cpp_code = """#include <iostream>
using namespace std;
int main() {
    cout << "Hello from Docker C++!" << endl;
    return 0;
}"""
        
        # Criar diretório temporário
        with tempfile.TemporaryDirectory() as temp_dir:
            # Escrever código
            code_file = os.path.join(temp_dir, "solution.cpp")
            with open(code_file, 'w') as f:
                f.write(cpp_code)
            
            # Executar container
            container = client.containers.run(
                'adaptivejudge-cpp:latest',
                command=['sh', '-c', 'g++ -o solution solution.cpp && ./solution'],
                volumes={temp_dir: {'bind': '/workspace', 'mode': 'rw'}},
                working_dir='/workspace',
                remove=True,
                capture_output=True,
                text=True
            )
            
            print(f"  ✓ Container executado com sucesso")
            print(f"  ✓ Output: {container.decode('utf-8').strip()}")
            return True
            
    except Exception as e:
        print(f"  ✗ Erro testando C++: {e}")
        return False

def test_python_image(client):
    """Teste da imagem Python."""
    print("\n🐍 Testando imagem Python...")
    
    try:
        # Verificar se a imagem existe
        try:
            image = client.images.get('adaptivejudge-python:latest')
            print(f"  ✓ Imagem encontrada: {image.short_id}")
        except docker.errors.ImageNotFound:
            print("  ✗ Imagem adaptivejudge-python:latest não encontrada")
            return False
        
        # Código Python simples
        python_code = "print('Hello from Docker Python!')"
        
        # Criar diretório temporário
        with tempfile.TemporaryDirectory() as temp_dir:
            # Escrever código
            code_file = os.path.join(temp_dir, "solution.py")
            with open(code_file, 'w') as f:
                f.write(python_code)
            
            # Executar container
            container = client.containers.run(
                'adaptivejudge-python:latest',
                command=['python3', 'solution.py'],
                volumes={temp_dir: {'bind': '/workspace', 'mode': 'rw'}},
                working_dir='/workspace',
                remove=True,
                capture_output=True,
                text=True
            )
            
            print(f"  ✓ Container executado com sucesso")
            print(f"  ✓ Output: {container.decode('utf-8').strip()}")
            return True
            
    except Exception as e:
        print(f"  ✗ Erro testando Python: {e}")
        return False

def test_problem_solving():
    """Teste resolução de problema."""
    print("\n📝 Testando resolução de problema...")
    
    try:
        client = docker.from_env()
        
        # Problema: somar dois números
        input_data = "5 3"
        expected_output = "8"
        
        # Solução Python
        python_solution = """
a, b = map(int, input().split())
print(a + b)
"""
        
        # Solução C++
        cpp_solution = """#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}"""
        
        results = {}
        
        # Testar Python
        with tempfile.TemporaryDirectory() as temp_dir:
            # Arquivos
            code_file = os.path.join(temp_dir, "solution.py")
            input_file = os.path.join(temp_dir, "input.txt")
            
            with open(code_file, 'w') as f:
                f.write(python_solution)
            with open(input_file, 'w') as f:
                f.write(input_data)
            
            # Executar
            container = client.containers.run(
                'adaptivejudge-python:latest',
                command=['sh', '-c', 'python3 solution.py < input.txt'],
                volumes={temp_dir: {'bind': '/workspace', 'mode': 'rw'}},
                working_dir='/workspace',
                remove=True,
                capture_output=True,
                text=True
            )
            
            python_output = container.decode('utf-8').strip()
            results['python'] = python_output == expected_output
            print(f"  🐍 Python: {python_output} {'✓' if results['python'] else '✗'}")
        
        # Testar C++
        with tempfile.TemporaryDirectory() as temp_dir:
            # Arquivos
            code_file = os.path.join(temp_dir, "solution.cpp")
            input_file = os.path.join(temp_dir, "input.txt")
            
            with open(code_file, 'w') as f:
                f.write(cpp_solution)
            with open(input_file, 'w') as f:
                f.write(input_data)
            
            # Executar
            container = client.containers.run(
                'adaptivejudge-cpp:latest',
                command=['sh', '-c', 'g++ -o solution solution.cpp && ./solution < input.txt'],
                volumes={temp_dir: {'bind': '/workspace', 'mode': 'rw'}},
                working_dir='/workspace',
                remove=True,
                capture_output=True,
                text=True
            )
            
            cpp_output = container.decode('utf-8').strip()
            results['cpp'] = cpp_output == expected_output
            print(f"  🔧 C++: {cpp_output} {'✓' if results['cpp'] else '✗'}")
        
        return all(results.values())
        
    except Exception as e:
        print(f"  ✗ Erro testando resolução: {e}")
        return False

def main():
    """Execute todos os testes."""
    print("🎯 TESTE SIMPLES - DOCKER IMAGES")
    print("=" * 50)
    
    # Teste conexão Docker
    client = test_docker_connection()
    if not client:
        print("\n❌ Docker não disponível!")
        return 1
    
    success = True
    
    # Teste imagens
    success &= test_cpp_image(client)
    success &= test_python_image(client)
    
    # Teste resolução de problema
    success &= test_problem_solving()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TODOS OS TESTES DOCKER PASSARAM!")
        print("\n✅ As imagens Docker estão funcionando corretamente!")
        print("🚀 Sistema pronto para execução de código!")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("\nVerifique se as imagens foram construídas corretamente.")
    
    return 0 if success else 1

if __name__ == '__main__':
    exit(main())
