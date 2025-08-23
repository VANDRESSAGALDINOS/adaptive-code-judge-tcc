#!/usr/bin/env /usr/bin/python3
"""
Script para criar submissions de exemplo no banco de dados
"""
import sys
import os
import random
from datetime import datetime, timedelta

# Adiciona o diretório src ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from models import db
from models.problem import Problem
from models.submission import Submission
from models.submission_result import SubmissionTestResult, ErrorType
from models.test_case import TestCase
from config.database import DatabaseConfig
from flask import Flask

def create_app():
    """Cria a aplicação Flask"""
    app = Flask(__name__)
    
    # Configura o banco de dados
    config = DatabaseConfig.get_config()
    app.config.update(config)
    
    # Inicializa o SQLAlchemy
    db.init_app(app)
    
    return app

def create_sample_submissions():
    """Cria submissions de exemplo para os problemas existentes"""
    
    app = create_app()
    
    with app.app_context():
        print("🚀 Criando submissions de exemplo...")
        
        # Busca todos os problemas
        problems = Problem.query.all()
        print(f"📚 Encontrados {len(problems)} problemas")
        
        # Códigos de exemplo
        cpp_codes = [
            '''#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}''',
            '''#include <iostream>
#include <vector>
using namespace std;
int main() {
    cout << "Hello, World!" << endl;
    return 0;
}''',
            '''#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    for(int i = 1; i <= n; i++) {
        cout << i << " ";
    }
    return 0;
}'''
        ]
        
        python_codes = [
            '''a, b = map(int, input().split())
print(a + b)''',
            '''print("Hello, World!")''',
            '''n = int(input())
for i in range(1, n+1):
    print(i, end=" ")''',
            '''# Código com erro proposital
a, b = map(int, input().split()
print(a + b)  # Erro de sintaxe - parênteses''',
            '''# Código que pode dar TLE
import time
a, b = map(int, input().split())
time.sleep(2)  # Simula TLE
print(a + b)'''
        ]
        
        submissions_created = 0
        results_created = 0
        
        for problem in problems:
            print(f"\n📝 Criando submissions para: {problem.title}")
            
            # Cria 2-4 submissions por problema
            num_submissions = random.randint(2, 4)
            
            for i in range(num_submissions):
                # Alterna entre linguagens
                language = 'cpp' if i % 2 == 0 else 'python'
                
                # Seleciona código baseado na linguagem
                if language == 'cpp':
                    source_code = random.choice(cpp_codes)
                else:
                    source_code = random.choice(python_codes)
                
                # Determina status e resultado baseado no código
                if 'erro' in source_code.lower() or 'sleep' in source_code:
                    status = 'FAILED'
                    if 'sleep' in source_code:
                        result = 'TLE'
                        error_message = 'Time Limit Exceeded'
                    else:
                        result = 'CE'
                        error_message = 'Compilation Error: Syntax error'
                    execution_time = 0.0
                    memory_usage = 0
                else:
                    # Submissão bem-sucedida
                    status = 'COMPLETED'
                    result = 'AC'
                    error_message = None
                    execution_time = random.uniform(0.1, 1.5)
                    memory_usage = random.randint(1024, 8192)  # KB
                
                # Data aleatória nos últimos 30 dias
                created_at = datetime.now() - timedelta(days=random.randint(0, 30))
                
                submission = Submission(
                    problem_id=problem.id,
                    language=language,
                    source_code=source_code,
                    status=status,
                    result=result,
                    execution_time_total=execution_time,
                    memory_usage_max=memory_usage,
                    error_message=error_message,
                    docker_image=f'adaptive-judge-{language}:latest',
                    container_id=f'container_{random.randint(10000, 99999)}' if status == 'COMPLETED' else None,
                    created_at=created_at,
                    updated_at=created_at
                )
                
                db.session.add(submission)
                db.session.flush()  # Para obter o ID
                
                print(f"   ✅ Submission {language} criada - Status: {status}, Resultado: {result}")
                submissions_created += 1
                
                # Cria resultados de teste para esta submission
                test_cases = problem.test_cases
                for test_case in test_cases:
                    if status == 'COMPLETED':
                        # Simula execução bem-sucedida na maioria dos casos
                        passed = random.choice([True, True, True, False])  # 75% de sucesso
                        if passed:
                            error_type = None
                            output_diff = None
                            stderr = None
                        else:
                            error_type = random.choice([ErrorType.WA, ErrorType.TLE, ErrorType.MLE])
                            output_diff = "Expected: 8, Got: 7" if error_type == ErrorType.WA else None
                            stderr = f"Error: {error_type.value}" if error_type != ErrorType.WA else None
                        
                        test_execution_time = random.uniform(0.05, execution_time/len(test_cases))
                        test_memory = random.randint(memory_usage//2, memory_usage)
                        stdout = "8" if passed else "7"
                        
                    else:
                        # Submission falhou - todos os testes falharam
                        passed = False
                        if result == 'CE':
                            error_type = ErrorType.CE
                            stdout = None
                            stderr = error_message
                        elif result == 'TLE':
                            error_type = ErrorType.TLE
                            stdout = None
                            stderr = "Process killed: time limit exceeded"
                        else:
                            error_type = ErrorType.RE
                            stdout = None
                            stderr = "Runtime error occurred"
                        
                        output_diff = None
                        test_execution_time = 0.0
                        test_memory = 0
                    
                    test_result = SubmissionTestResult(
                        submission_id=submission.id,
                        test_case_id=test_case.id,
                        passed=passed,
                        execution_time=test_execution_time,
                        memory_usage=test_memory,
                        error_type=error_type,
                        output_diff=output_diff,
                        stdout=stdout,
                        stderr=stderr
                    )
                    
                    db.session.add(test_result)
                    results_created += 1
        
        # Salva todas as mudanças
        db.session.commit()
        print(f"\n✅ {submissions_created} submissions criadas!")
        print(f"✅ {results_created} resultados de teste criados!")
        
        # Mostra estatísticas finais
        print("\n📊 ESTATÍSTICAS FINAIS:")
        total_problems = Problem.query.count()
        total_submissions = Submission.query.count()
        total_results = SubmissionTestResult.query.count()
        
        print(f"   📚 Problemas: {total_problems}")
        print(f"   🚀 Submissions: {total_submissions}")
        print(f"   🧪 Resultados de teste: {total_results}")
        
        # Estatísticas por linguagem
        print("\n📊 SUBMISSIONS POR LINGUAGEM:")
        cpp_count = Submission.query.filter_by(language='cpp').count()
        python_count = Submission.query.filter_by(language='python').count()
        print(f"   🔧 C++: {cpp_count}")
        print(f"   🐍 Python: {python_count}")
        
        # Estatísticas por resultado
        print("\n📊 RESULTADOS:")
        ac_count = Submission.query.filter_by(result='AC').count()
        ce_count = Submission.query.filter_by(result='CE').count()
        tle_count = Submission.query.filter_by(result='TLE').count()
        print(f"   ✅ Aceitas (AC): {ac_count}")
        print(f"   🚫 Erro de Compilação (CE): {ce_count}")
        print(f"   ⏰ Tempo Limite (TLE): {tle_count}")

if __name__ == "__main__":
    print("🎯 CRIADOR DE SUBMISSIONS - ADAPTIVE CODE JUDGE")
    print("=" * 60)
    
    try:
        create_sample_submissions()
        print(f"\n🎉 PROCESSO CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
