# Ambiente de execucao (registro para reprodutibilidade - S3.8)

Registro do ambiente exato em que TODOS os experimentos (eixo teorico + real-world)
foram executados. Numeros conferidos no momento (nao inventados).

## Imagens Docker (buildadas em 2026-05-27, locais)
- `adaptive-judge-cpp:latest`  - image id `sha256:543fdcbc0432edf5ccaa424eeabf1b176d91487404272b7b016137df8c43e62e`
- `adaptive-judge-python:latest` - image id `sha256:a15c27128ffb6f9a91f074acb01e1ac09486381109d610bfd867524c0c3a77a9`

## Base fixada (Dockerfiles em docker/)
- C++:    `FROM gcc:16.1.0`          (antes era `gcc:latest`, tag flutuante)
- Python: `FROM python:3.11.15-slim` (antes era `python:3.11-slim`, patch flutuante)

## Toolchain (conferido dentro das imagens)
- Compilador C++: g++ (GCC) **16.1.0**   [ATENCAO: NAO e 13.x - o texto antigo estava errado]
- Interpretador:  Python **3.11.15**
- libc:           Debian GLIBC **2.41** (Debian 13)

## Plataforma
- Kernel do container (runtime): Linux **6.12.54-linuxkit**
- Arquitetura: **aarch64 / arm64** (Apple Silicon)
- Host: Darwin 24.6.0 arm64 (macOS, Docker Desktop)

## Parametros de execucao (iguais em todos os pipelines)
- Compilacao C++: flag `-O2`
- Memoria: `512m` | CPUs: `1.0`
- Pilha (recursao profunda): `ulimit -s 256MB` aplicado pelo engine (S3.1/S3.8)
- Timer: `date +%s.%N` (resolucao ~microssegundo), execucao so (startup/compilacao fora)
- Bootstrap IC95: 10.000 resamples, seed 42

## Nota de honestidade (para a redacao de S3.6/S3.8)
- As imagens estao fixadas por **VERSAO** (gcc:16.1.0, python:3.11.15-slim), NAO por
  digest sha256 de registry. Motivo: sao imagens locais; as bases originais nao foram
  retidas localmente e re-puxar `:latest` traria versao diferente. A fixacao por versao
  ja elimina o furo maior (a deriva de versao MAIOR do `gcc:latest`, que hoje aponta p/ GCC 16).
- Portanto, no artigo: escrever **"imagens baseadas em gcc:16.1.0 e python:3.11.15-slim,
  versoes fixadas"** - NAO "fixadas por digest". Digest pinning de registry = trabalho futuro.
- Validade externa nao depende de bit-a-bit: mede-se uma RAZAO (beta) com as duas linguagens
  no MESMO ambiente; recalibra-se por ambiente (ver S3.6). arm64 vs x86 muda beta absoluto,
  nao as conclusoes qualitativas.
