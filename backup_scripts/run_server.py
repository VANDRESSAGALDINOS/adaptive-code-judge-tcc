#!/usr/bin/env python3
"""
Script para inicializar o servidor Adaptive Code Judge.
Este script resolve os problemas de imports relativos.
"""

import sys
import os

# Adicionar o diretório src ao path para imports absolutos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configurar variáveis de ambiente
os.environ.setdefault('SQLITE_PATH', os.path.join(os.path.dirname(__file__), 'data', 'adaptive_judge.db'))

def main():
    """Inicializar e executar o servidor."""
    try:
        # Importar após configurar o path
        from main import main as app_main
        
        print("🚀 Iniciando Adaptive Code Judge...")
        print(f"📁 Diretório: {os.path.dirname(__file__)}")
        print(f"💾 Database: {os.environ.get('SQLITE_PATH')}")
        print()
        
        # Executar aplicação
        app_main()
        
    except ImportError as e:
        print(f"❌ Erro de import: {e}")
        print("\n🔧 Tentando corrigir estrutura de imports...")
        
        # Tentar corrigir imports em tempo real
        fix_imports()
        
        # Tentar novamente
        from main import main as app_main
        app_main()
        
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def fix_imports():
    """Corrigir imports relativos nos arquivos da API."""
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    
    # Arquivos que precisam de correção
    files_to_fix = [
        'api/problems.py',
        'api/submissions.py', 
        'api/benchmarks.py',
        'api/health.py',
        'api/__init__.py',
        'services/benchmark_service.py',
        'services/submission_service.py',
        'executor/docker_executor.py'
    ]
    
    import_fixes = {
        'from ..services.problem_service import ProblemService': 'from services.problem_service import ProblemService',
        'from ..services.submission_service import SubmissionService': 'from services.submission_service import SubmissionService',
        'from ..services.benchmark_service import BenchmarkService': 'from services.benchmark_service import BenchmarkService',
        'from ..models import': 'from models import',
        'from ..config.app import AppConfig': 'from config.app import AppConfig',
        'from ..executor import': 'from executor import',
        'from .problems import problems_bp': 'from api.problems import problems_bp',
        'from .submissions import submissions_bp': 'from api.submissions import submissions_bp',
        'from .benchmarks import benchmarks_bp': 'from api.benchmarks import benchmarks_bp',
        'from .health import health_bp': 'from api.health import health_bp',
    }
    
    for file_path in files_to_fix:
        full_path = os.path.join(src_dir, file_path)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r') as f:
                    content = f.read()
                
                # Aplicar correções
                for old_import, new_import in import_fixes.items():
                    content = content.replace(old_import, new_import)
                
                with open(full_path, 'w') as f:
                    f.write(content)
                
                print(f"  ✓ Corrigido: {file_path}")
                
            except Exception as e:
                print(f"  ✗ Erro corrigindo {file_path}: {e}")

if __name__ == '__main__':
    main()
