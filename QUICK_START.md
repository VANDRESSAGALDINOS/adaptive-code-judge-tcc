# ⚡ Quick Start - Adaptive Code Judge

## 🚀 **Início Rápido (5 minutos)**

### 1. **Verificar Pré-requisitos**
```bash
python3 --version    # Deve ser 3.9+
docker --version     # Docker instalado
./run.sh test       # Testar sistema
```

### 2. **Iniciar Sistema**
```bash
./run.sh server     # Inicia em http://localhost:8000
```

### 3. **Testar API**
```bash
# Em outro terminal
curl http://localhost:8000/
curl http://localhost:8000/api/problems
```

## 🧪 **Comandos Essenciais**

| Comando | Função |
|---------|--------|
| `./run.sh test` | ✅ Teste completo do sistema |
| `./run.sh server` | 🚀 Iniciar servidor web |
| `./run.sh demo` | 🎬 Demonstração completa |
| `./run.sh docker-test` | 🐳 Testar Docker |
| `./run.sh health` | 🏥 Status do servidor |

## 📋 **Checklist de Verificação**

- [ ] Python 3.9.6 funcionando (`python3 --version`)
- [ ] Docker disponível (`docker --version`) 
- [ ] Imagens construídas (`docker images | grep adaptivejudge`)
- [ ] Teste passou (`./run.sh test`)
- [ ] Servidor iniciou (`./run.sh server`)
- [ ] API responde (`curl http://localhost:8000/`)

## 🆘 **Problemas Comuns**

### **"No module named 'flask'"**
```bash
pip3 install -r requirements.txt
```

### **Docker não encontrado** 
```bash
brew install --cask docker
open /Applications/Docker.app
```

### **Imagens Docker não existem**
```bash
cd docker
docker build -t adaptivejudge-cpp:latest -f Dockerfile.cpp .
docker build -t adaptivejudge-python:latest -f Dockerfile.python .
```

### **Porta 8000 ocupada**
```bash
pkill -f "start_server.py"
./run.sh server
```

## ✅ **Sistema Funcionando = Todos estes OK:**

1. ✅ `./run.sh test` → "TODOS OS TESTES PRINCIPAIS PASSARAM!"
2. ✅ `./run.sh docker-test` → "Hello Docker Python!" e "Hello Docker C++!"
3. ✅ `./run.sh server` → Servidor iniciando
4. ✅ `curl http://localhost:8000/` → JSON com "Adaptive Code Judge"

## 🎯 **Uso Básico da API**

```bash
# 1. Listar problemas
curl http://localhost:8000/api/problems

# 2. Ver problema específico  
curl http://localhost:8000/api/problems/1

# 3. Submeter código Python
curl -X POST http://localhost:8000/api/submissions/judge \
  -H "Content-Type: application/json" \
  -d '{
    "problem_id": 1,
    "language": "python", 
    "source_code": "print(\"Hello World!\")"
  }'
```

## 📖 **Documentação Completa**

Ver `README.md` para documentação detalhada com todos os endpoints, testes e funcionalidades.

---
**🚀 Em 5 minutos você tem um sistema completo de avaliação de código funcionando!**
