#!/bin/bash
# Script para executar o Adaptive Code Judge com a versao correta do Python

export PYTHON_CMD="/usr/bin/python3"

echo "Adaptive Code Judge Launcher"
echo "Using Python: $($PYTHON_CMD --version)"
echo ""

case "$1" in
    "server"|"start")
        echo "Starting server..."
        $PYTHON_CMD start_server.py
        ;;
    "docker-test")
        echo "Testing Docker images directly..."
        echo 'print("Hello Docker Python!")' > /tmp/test.py
        docker run --rm -v /tmp:/workspace -w /workspace adaptive-judge-python:latest python3 test.py
        echo 'echo "Hello Docker C++!"' > /tmp/test.sh
        docker run --rm -v /tmp:/workspace -w /workspace adaptive-judge-cpp:latest bash test.sh
        ;;
    "health")
        echo "Verificando saude do sistema..."
        sleep 2
        curl -s http://localhost:8000/health || echo "Servidor nao esta rodando"
        ;;
    *)
        echo "Uso: ./run.sh [comando]"
        echo ""
        echo "Comandos disponiveis:"
        echo "  server      - Iniciar o servidor web"
        echo "  docker-test - Testar as imagens Docker diretamente"
        echo "  health      - Verificar status do servidor"
        echo ""
        echo "Exemplos:"
        echo "  ./run.sh server    # Inicia o servidor"
        echo "  ./run.sh health    # Verifica o servidor"
        ;;
esac
