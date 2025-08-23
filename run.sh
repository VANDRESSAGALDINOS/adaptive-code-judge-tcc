#!/bin/bash
# Script para executar o Adaptive Code Judge com a versão correta do Python

export PYTHON_CMD="/usr/bin/python3"

echo "🚀 Adaptive Code Judge Launcher"
echo "🐍 Usando Python: $($PYTHON_CMD --version)"
echo ""

case "$1" in
    "server"|"start")
        echo "📡 Iniciando servidor..."
        $PYTHON_CMD start_server.py
        ;;
    "test")
        echo "🧪 Executando testes completos..."
        $PYTHON_CMD test.py
        ;;
    "demo")
        echo "🎬 Executando demonstração..."
        $PYTHON_CMD demo_final.py
        ;;
    "docker-test")
        echo "🐳 Testando Docker..."
        echo "Testando execução direta via Docker..."
        echo 'print("Hello Docker Python!")' > /tmp/test.py
        docker run --rm -v /tmp:/workspace -w /workspace adaptivejudge-python:latest python3 test.py
        echo 'echo "Hello Docker C++!"' > /tmp/test.sh
        docker run --rm -v /tmp:/workspace -w /workspace adaptivejudge-cpp:latest bash test.sh
        ;;
    "health")
        echo "🏥 Verificando saúde do sistema..."
        sleep 2
        curl -s http://localhost:8000/health || echo "Servidor não está rodando"
        ;;
    *)
        echo "📋 Uso: ./run.sh [comando]"
        echo ""
        echo "Comandos disponíveis:"
        echo "  server     - Iniciar o servidor web"
        echo "  test       - Executar testes completos do sistema"
        echo "  demo       - Executar demonstração completa"
        echo "  docker-test- Testar Docker images diretamente"
        echo "  health     - Verificar status do servidor"
        echo ""
        echo "Exemplos:"
        echo "  ./run.sh server    # Inicia o servidor"
        echo "  ./run.sh test      # Executa testes"
        ;;
esac
