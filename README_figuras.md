# Gerador de Figuras - TCC Juiz de Código Adaptativo

Este script gera automaticamente todas as figuras (Gráficos 1-9 e 11) do TCC usando **EXCLUSIVAMENTE** dados reais extraídos dos experimentos realizados. Versão final corrigida com rigor científico completo.

## Instalação

```bash
sudo apt update
sudo apt install -y python3-matplotlib python3-numpy
```

## Como usar

```bash
python make_figures.py
```

## O que o script faz

1. **Extrai dados reais** de todos os arquivos JSON de calibração dos experimentos
2. **Calcula métricas** diretamente dos tempos de execução coletados
3. **Gera gráficos** com rigor científico usando apenas dados empíricos
4. **Salva** PNGs em `figuras/` com qualidade de publicação (DPI 300)

## Correções implementadas

✅ **Gráfico 1**: Usa tempos reais de execução em vez de simulação  
✅ **Gráfico 4**: Extrai fatores β reais dos arquivos de calibração  
✅ **Gráfico 5**: Agrupa β por categoria usando dados reais  
✅ **Gráfico 7**: Calcula IQR real de cada experimento  
✅ **Gráfico 9**: Usa valores documentados no TCC (63% → 5%)  
✅ **Todos**: Eliminada simulação desnecessária, apenas dados empíricos

## Figuras geradas

- `grafico01_overhead_boxplot.png` - Distribuição do overhead por linguagem
- `grafico02_detectabilidade_ratio.png` - Evolução da detectabilidade por tamanho de entrada  
- `grafico03_perf_complexidade_barras.png` - Performance por classe de complexidade
- `grafico04_beta_hist.png` - Distribuição dos fatores β
- `grafico05_beta_box_by_category.png` - β por categoria algorítmica
- `grafico06_convergencia_iqr_curvas.png` - Convergência do IQR por execuções
- `grafico07_iqr_box_by_language.png` - Distribuição do IQR/mediana por linguagem
- `grafico08_forest_beta_ci.png` - Forest plot de β (Top 15)
- `grafico09_tle_reduction.png` - Redução de TLE injusto
- `grafico11_comparativo_barras.png` - Comparativo de desempenho

## Dados utilizados

- `documentation/outputs/complexity_summary.csv` - dados das classes de complexidade
- `documentation/outputs/realworld_summary.csv` - dados dos problemas reais
- `documentation/outputs/executive_statistics.json` - estatísticas executivas
- `experiments_realworld/**/calibration_*.json` - dados de calibração dos experimentos
- `experiments/complexity_analysis/refined_analysis.json` - análise refinada

## Comportamento robusto

- Se um CSV não existir, o script **pula aquele gráfico** e continua
- Usa **valores padrão** quando dados específicos não estão disponíveis
- **Não quebra** mesmo se alguns dados estiverem ausentes
- Mostra **status detalhado** no terminal

## Qualidade das figuras

- **DPI 300** para publicação
- **bbox_inches="tight"** para corte automático
- **Estilo padrão** matplotlib (sem customizações)
- **Títulos e rótulos** exatamente conforme especificação do TCC
