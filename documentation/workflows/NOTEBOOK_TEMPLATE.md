# Esqueleto do Notebook Python Final - TCC Analysis

## 📊 Estrutura do `final_analysis.ipynb`

### Cell 1: Setup e Imports
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# Configuração visual
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
```

### Cell 2: Carregamento de Dados
```python
def load_all_experiments():
    """Carrega dados de todos os experimentos"""
    experiments = []
    
    for categoria_path in Path('experiments_realworld').iterdir():
        if categoria_path.is_dir() and categoria_path.name in ['graphs', 'dp_iterativa', 'dp_recursiva', 'recursao_profunda', 'backtracking']:
            for problema_path in categoria_path.iterdir():
                if problema_path.is_dir():
                    metadata_file = problema_path / 'metadata_graficos.json'
                    if metadata_file.exists():
                        with open(metadata_file) as f:
                            data = json.load(f)
                            experiments.append(data)
    
    return pd.DataFrame(experiments)

df = load_all_experiments()
print(f"Carregados {len(df)} experimentos válidos")
```

### Cell 3: Gráfico Executivo - Fatores por Categoria
```python
def plot_fatores_categoria(df):
    """Gráfico 1: Fatores de Ajuste por Categoria Algorítmica"""
    
    # Agrupar por categoria
    categoria_stats = df.groupby('categoria').agg({
        'fator_ajuste': ['median', 'std', 'count']
    }).round(2)
    
    # Gráfico de barras com error bars
    fig, ax = plt.subplots(figsize=(12, 8))
    
    categorias = categoria_stats.index
    medianas = categoria_stats[('fator_ajuste', 'median')]
    erros = categoria_stats[('fator_ajuste', 'std')]
    
    bars = ax.bar(categorias, medianas, yerr=erros, capsize=5, 
                  color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57'])
    
    ax.set_ylabel('Fator de Ajuste (x)', fontsize=12)
    ax.set_xlabel('Categoria Algorítmica', fontsize=12)
    ax.set_title('Diversidade de Fatores por Categoria\n(Evidência contra fator único)', fontsize=14, pad=20)
    
    # Linha horizontal em 3x (fator "comum")
    ax.axhline(y=3, color='red', linestyle='--', alpha=0.7, label='Fator fixo típico (3x)')
    
    # Anotações
    for bar, mediana in zip(bars, medianas):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{mediana:.1f}x', ha='center', va='bottom', fontweight='bold')
    
    ax.legend()
    ax.set_ylim(0, min(25, max(medianas) * 1.2))  # Escala responsável
    
    plt.tight_layout()
    plt.savefig('outputs/fatores_por_categoria.png', dpi=300, bbox_inches='tight')
    plt.show()

plot_fatores_categoria(df)
```

### Cell 4: Heatmap de Injustiça
```python
def plot_heatmap_injustica(df):
    """Gráfico 2: Mapa de Injustiça Sistemática"""
    
    # Preparar dados para heatmap
    heatmap_data = []
    for _, row in df.iterrows():
        for size_name, size_data in row['injustica_por_tamanho'].items():
            heatmap_data.append({
                'categoria': row['categoria'],
                'input_size': f"N={size_data['size']:,}",
                'tle_rate': size_data['tle_rate'] * 100
            })
    
    heatmap_df = pd.DataFrame(heatmap_data)
    pivot_df = heatmap_df.pivot(index='categoria', columns='input_size', values='tle_rate')
    
    # Criar heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(pivot_df, annot=True, fmt='.0f', cmap='RdYlGn_r', 
                cbar_kws={'label': '% Python TLE'}, ax=ax)
    
    ax.set_title('Mapa de Injustiça Sistemática\n(% TLE Python por Categoria vs Tamanho Input)', 
                 fontsize=14, pad=20)
    ax.set_xlabel('Tamanho do Input', fontsize=12)
    ax.set_ylabel('Categoria Algorítmica', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('outputs/heatmap_injustica.png', dpi=300, bbox_inches='tight')
    plt.show()

plot_heatmap_injustica(df)
```

### Cell 5: Validação Externa
```python
def plot_validacao_externa(df):
    """Gráfico 3: Validação vs CSES Real"""
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Scatter plot
    x = df['validacao_cses_real']
    y = df['validacao_nosso_benchmark'] 
    categorias = df['categoria']
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
    categoria_colors = {cat: colors[i] for i, cat in enumerate(df['categoria'].unique())}
    
    for categoria in df['categoria'].unique():
        mask = categorias == categoria
        ax.scatter(x[mask], y[mask], label=categoria, 
                  color=categoria_colors[categoria], s=100, alpha=0.7)
    
    # Linha de validação perfeita (y=x)
    lims = [0, max(max(x), max(y)) * 1.1]
    ax.plot(lims, lims, 'k--', alpha=0.75, zorder=0, label='Validação perfeita (y=x)')
    
    # Banda de confiança
    ax.fill_between(lims, [l*0.8 for l in lims], [l*1.2 for l in lims], 
                    alpha=0.2, color='gray', label='Banda aceitável (±20%)')
    
    ax.set_xlabel('% TLE Python (CSES Real)', fontsize=12)
    ax.set_ylabel('% TLE Python (Nosso Benchmark)', fontsize=12)
    ax.set_title('Validação Externa: CSES Real vs Nosso Benchmark\n(R² = correlação)', fontsize=14, pad=20)
    
    # Calcular R²
    correlation = np.corrcoef(x, y)[0, 1]
    r_squared = correlation ** 2
    ax.text(0.05, 0.95, f'R² = {r_squared:.3f}', transform=ax.transAxes, 
            fontsize=12, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax.legend()
    ax.set_xlim(0, lims[1])
    ax.set_ylim(0, lims[1])
    
    plt.tight_layout()
    plt.savefig('outputs/validacao_externa.png', dpi=300, bbox_inches='tight')
    plt.show()

plot_validacao_externa(df)
```

### Cell 6: Before/After Comparison
```python
def plot_before_after(df):
    """Gráfico 4: Correção Responsável (Before/After)"""
    
    categorias = df['categoria'].unique()
    x = np.arange(len(categorias))
    width = 0.35
    
    tradicional = [df[df['categoria']==cat]['tradicional_python_rate'].mean() for cat in categorias]
    adaptativo = [df[df['categoria']==cat]['adaptativo_python_rate'].mean() for cat in categorias]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bars1 = ax.bar(x - width/2, tradicional, width, label='Sistema Tradicional', 
                   color='#FF6B6B', alpha=0.8)
    bars2 = ax.bar(x + width/2, adaptativo, width, label='Sistema Adaptativo', 
                   color='#4ECDC4', alpha=0.8)
    
    # Anotações de melhoria
    for i, (trad, adapt) in enumerate(zip(tradicional, adaptativo)):
        melhoria = adapt - trad
        ax.annotate(f'+{melhoria:.0f}pp', xy=(i, max(trad, adapt) + 5), 
                   ha='center', fontweight='bold', color='green')
    
    ax.set_ylabel('% Success Rate Python', fontsize=12)
    ax.set_xlabel('Categoria Algorítmica', fontsize=12)
    ax.set_title('Correção de Injustiça: Sistema Adaptativo\n(Melhoria sem comprometer rigor)', 
                 fontsize=14, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categorias, rotation=45)
    ax.legend()
    ax.set_ylim(0, 105)
    
    # Linha em 100%
    ax.axhline(y=100, color='gray', linestyle=':', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('outputs/before_after.png', dpi=300, bbox_inches='tight')
    plt.show()

plot_before_after(df)
```

### Cell 7: Casos Emblemáticos
```python
def plot_casos_emblematicos(df):
    """Casos individuais narrativos"""
    
    # Filtrar casos de alta prioridade
    alta_prioridade = df[df['prioridade_graficos'] == 'Alta'].head(3)
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    for i, (_, caso) in enumerate(alta_prioridade.iterrows()):
        ax = axes[i]
        
        # Plot específico do caso
        tempos_cpp = caso['tempos_cpp']  # Extrair dos dados
        tempos_python = caso['tempos_python']
        
        ax.hist([tempos_cpp, tempos_python], bins=20, alpha=0.7, 
               label=['C++', 'Python'], color=['blue', 'orange'])
        
        ax.axvline(x=1.0, color='red', linestyle='--', label='Limite (1.0s)')
        ax.set_title(f"{caso['categoria']}\n{caso['problema']}\n(Fator: {caso['fator_ajuste']:.1f}x)")
        ax.set_xlabel('Tempo (s)')
        ax.set_ylabel('Frequência')
        ax.legend()
    
    plt.tight_layout()
    plt.savefig('outputs/casos_emblematicos.png', dpi=300, bbox_inches='tight')
    plt.show()

plot_casos_emblematicos(df)
```

### Cell 8: Estatísticas Finais
```python
def generate_final_stats(df):
    """Gerar estatísticas executivas para TCC"""
    
    stats = {
        'total_experiments': len(df),
        'total_categories': df['categoria'].nunique(),
        'avg_adjustment_factor': df['fator_ajuste'].mean(),
        'max_adjustment_factor': df['fator_ajuste'].max(),
        'min_adjustment_factor': df['fator_ajuste'].min(),
        'correlation_with_cses': np.corrcoef(df['validacao_cses_real'], 
                                           df['validacao_nosso_benchmark'])[0,1],
        'selectivity_preserved_rate': df['seletividade_preservada'].mean() * 100,
        'avg_python_improvement': (df['adaptativo_python_rate'] - df['tradicional_python_rate']).mean()
    }
    
    print("📊 ESTATÍSTICAS FINAIS PARA TCC:")
    print("=" * 50)
    print(f"Total de experimentos: {stats['total_experiments']}")
    print(f"Categorias testadas: {stats['total_categories']}")
    print(f"Fator de ajuste médio: {stats['avg_adjustment_factor']:.1f}x")
    print(f"Range de fatores: {stats['min_adjustment_factor']:.1f}x - {stats['max_adjustment_factor']:.1f}x")
    print(f"Correlação com CSES: R = {stats['correlation_with_cses']:.3f}")
    print(f"Seletividade preservada: {stats['selectivity_preserved_rate']:.0f}% dos casos")
    print(f"Melhoria média Python: +{stats['avg_python_improvement']:.0f} pontos percentuais")
    
    # Salvar para uso no TCC
    with open('outputs/estatisticas_finais.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    return stats

final_stats = generate_final_stats(df)
```

### Cell 9: Export para LaTeX (TCC)
```python
def export_for_latex(df, stats):
    """Gerar tabelas e dados formatados para LaTeX"""
    
    # Tabela resumo por categoria
    categoria_summary = df.groupby('categoria').agg({
        'fator_ajuste': ['median', 'std', 'count'],
        'tradicional_python_rate': 'mean',
        'adaptativo_python_rate': 'mean'
    }).round(2)
    
    # Salvar como CSV para importar no LaTeX
    categoria_summary.to_csv('outputs/tabela_categorias.csv')
    
    # Gerar comandos LaTeX para estatísticas
    latex_commands = []
    latex_commands.append(f"\\newcommand{{\\totalexperiments}}{{{stats['total_experiments']}}}")
    latex_commands.append(f"\\newcommand{{\\avgfactor}}{{{stats['avg_adjustment_factor']:.1f}}}")
    latex_commands.append(f"\\newcommand{{\\correlationcses}}{{{stats['correlation_with_cses']:.3f}}}")
    latex_commands.append(f"\\newcommand{{\\pythonimprovement}}{{{stats['avg_python_improvement']:.0f}}}")
    
    with open('outputs/latex_commands.tex', 'w') as f:
        f.write('\n'.join(latex_commands))
    
    print("📄 Dados exportados para LaTeX em outputs/")

export_for_latex(df, final_stats)
```

## 📁 Estrutura de Output

```
outputs/
├── fatores_por_categoria.png     # Gráfico executivo
├── heatmap_injustica.png         # Mapa de TLEs
├── validacao_externa.png         # Scatter CSES
├── before_after.png              # Correção demonstrada
├── casos_emblematicos.png        # 3 casos narrativos
├── estatisticas_finais.json      # Dados numéricos
├── tabela_categorias.csv         # Para LaTeX
└── latex_commands.tex            # Comandos LaTeX
```

---
**Este notebook será executado APÓS todos os 15 experimentos estarem completos e validados!**

