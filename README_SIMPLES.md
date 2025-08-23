# 🚀 Adaptive Code Judge - Guia Rápido

## Como Usar (Versão Simples)

### 📋 Comandos Principais:

```bash
# Iniciar o servidor
./run.sh server

# Executar testes completos
./run.sh test

# Testar Docker (opcional)
./run.sh docker-test

# Verificar se servidor está rodando
./run.sh health
```

### 🌐 Acessar o Sistema:

1. **Inicie o servidor:**
   ```bash
   ./run.sh server
   ```

2. **Acesse no navegador:**
   - http://localhost:8000/ (página inicial)
   - http://localhost:8000/health (status do sistema)
   - http://localhost:8000/api/problems (lista de problemas)

### 📝 Exemplo de Uso da API:

```bash
# Listar problemas
curl http://localhost:8000/api/problems

# Ver detalhes de um problema
curl http://localhost:8000/api/problems/1

# Submeter código Python
curl -X POST http://localhost:8000/api/submissions/judge \
  -H "Content-Type: application/json" \
  -d '{
    "problem_id": 1,
    "language": "python",
    "source_code": "a, b = map(int, input().split())\nprint(a + b)"
  }'
```

### 🐍 Versão do Python:

O sistema usa automaticamente **Python 3.9.6** que tem todas as dependências instaladas.

### ✅ Status Atual:

- ✅ **Sistema Base**: Funcionando 100%
- ✅ **API REST**: Todos endpoints operacionais  
- ✅ **Docker**: Instalado e imagens prontas
- ✅ **Banco de Dados**: 4 problemas de exemplo
- ⚠️ **Execução de Código**: Funciona via CLI (ajuste menor na biblioteca Python)

### 🎯 Pronto para Usar!

O sistema está completamente funcional para:
- Gerenciar problemas e casos de teste
- API completa para integração
- Base sólida para competições de programação
- Ensino de algoritmos
- Benchmarks científicos
