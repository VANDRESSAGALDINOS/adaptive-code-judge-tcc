#!/usr/bin/env /usr/bin/python3
"""
Script para criar benchmarks de exemplo no banco de dados
"""
import sys
import os
import random
from datetime import datetime

# Adiciona o diretório src ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from models import db
from models.problem import Problem
from models.benchmark import Benchmark
from models.problem_benchmark_active import ProblemBenchmarkActive
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

def create_sample_benchmarks():
    """Cria benchmarks de exemplo para os problemas existentes"""
    
    app = create_app()
    
    with app.app_context():
        print("🔧 Criando benchmarks de exemplo...")
        
        # Busca todos os problemas
        problems = Problem.query.all()
        print(f"📚 Encontrados {len(problems)} problemas")
        
        benchmarks_created = 0
        
        for problem in problems:
            print(f"\n📝 Criando benchmark para: {problem.title}")
            
            # Verifica se já existe benchmark para este problema
            existing = Benchmark.query.filter_by(problem_id=problem.id).first()
            if existing:
                print(f"   ⚠️  Benchmark já existe, pulando...")
                continue
            
            # Cria dados simulados de benchmark
            base_time_cpp = random.uniform(0.1, 2.0)  # Entre 100ms e 2s
            adjustment_factor = random.uniform(1.2, 3.5)  # Python 20% a 250% mais lento
            
            # Simula medições com variabilidade
            median_cpp = base_time_cpp * random.uniform(0.95, 1.05)
            median_python = median_cpp * adjustment_factor * random.uniform(0.9, 1.1)
            
            iqr_cpp = median_cpp * random.uniform(0.03, 0.12)  # IQR de 3-12% (mais estável)
            iqr_python = median_python * random.uniform(0.05, 0.15)  # IQR de 5-15% (mais estável)
            
            # Determina se é confiável (critérios mais tolerantes)
            is_reliable = (iqr_cpp / median_cpp < 0.15) and (iqr_python / median_python < 0.20)
            
            # Precisa de um test case (usar o primeiro do problema)
            largest_test_case = problem.test_cases[0] if problem.test_cases else None
            if not largest_test_case:
                print(f"   ⚠️  Problema sem test cases, pulando...")
                continue
            
            from models.benchmark import BenchmarkStatus
            
            benchmark = Benchmark(
                problem_id=problem.id,
                largest_test_case_id=largest_test_case.id,
                base_time_cpp=round(base_time_cpp, 4),
                adjustment_factor_python=round(adjustment_factor, 3),
                status=BenchmarkStatus.STABLE,
                repetitions=10,
                python_median_time=round(median_python, 4),
                cpp_iqr=round(iqr_cpp, 4),
                python_iqr=round(iqr_python, 4),
                factor_cap=3.5,
                min_factor=1.2,
                is_reliable=is_reliable,
                cpp_status=BenchmarkStatus.STABLE,
                python_status=BenchmarkStatus.STABLE,
                cpp_times=f'[{", ".join([str(round(base_time_cpp * random.uniform(0.9, 1.1), 4)) for _ in range(10)])}]',
                python_times=f'[{", ".join([str(round(median_python * random.uniform(0.9, 1.1), 4)) for _ in range(10)])}]'
            )
            
            db.session.add(benchmark)
            print(f"   ✅ Benchmark criado:")
            print(f"      🕐 Tempo base C++: {benchmark.base_time_cpp}s")
            print(f"      🐍 Fator Python: {benchmark.adjustment_factor_python}x")
            print(f"      📊 Confiável: {'Sim' if benchmark.is_reliable else 'Não'}")
            
            benchmarks_created += 1
        
        # Salva as mudanças
        db.session.commit()
        print(f"\n✅ {benchmarks_created} benchmarks criados com sucesso!")
        
        # Ativa os benchmarks (cria relação many-to-many)
        print("\n🔗 Ativando benchmarks...")
        active_count = 0
        
        benchmarks = Benchmark.query.all()
        for benchmark in benchmarks:
            # Verifica se já está ativo
            existing_active = ProblemBenchmarkActive.query.filter_by(
                problem_id=benchmark.problem_id,
                benchmark_id=benchmark.id
            ).first()
            
            if not existing_active:
                active_relation = ProblemBenchmarkActive(
                    problem_id=benchmark.problem_id,
                    benchmark_id=benchmark.id
                )
                db.session.add(active_relation)
                active_count += 1
        
        db.session.commit()
        print(f"✅ {active_count} benchmarks ativados!")
        
        # Mostra estatísticas finais
        print("\n📊 ESTATÍSTICAS FINAIS:")
        total_problems = Problem.query.count()
        total_benchmarks = Benchmark.query.count()
        total_active = ProblemBenchmarkActive.query.count()
        
        print(f"   📚 Problemas: {total_problems}")
        print(f"   📊 Benchmarks: {total_benchmarks}")
        print(f"   🔗 Benchmarks ativos: {total_active}")
        
        # Mostra alguns exemplos
        print("\n📋 EXEMPLOS DE BENCHMARKS CRIADOS:")
        sample_benchmarks = Benchmark.query.limit(3).all()
        for benchmark in sample_benchmarks:
            problem = Problem.query.get(benchmark.problem_id)
            print(f"   📝 {problem.title}:")
            print(f"      C++: {benchmark.base_time_cpp}s | Python: {benchmark.adjustment_factor_python}x | Confiável: {'✅' if benchmark.is_reliable else '❌'}")

if __name__ == "__main__":
    print("🎯 CRIADOR DE BENCHMARKS - ADAPTIVE CODE JUDGE")
    print("=" * 60)
    
    try:
        create_sample_benchmarks()
        print(f"\n🎉 PROCESSO CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
