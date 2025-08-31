#!/usr/bin/env python3
"""
Script de Checklist para Experimentos - TCC Adaptive Code Judge
Executa após cada experimento para garantir coleta completa de dados
"""

import json
import os
from pathlib import Path
from datetime import datetime

class ExperimentChecklist:
    def __init__(self, experiment_path):
        self.path = Path(experiment_path)
        self.categoria = self.path.parent.name
        self.problema = self.path.name
        
    def check_required_files(self):
        """Verifica se todos os arquivos obrigatórios existem"""
        required_files = [
            'final_report.json',
            'results/calibration_*.json',
            'results/validation_results.json', 
            'results/slow_solution_validation.json',
            'resultados_finais/README.md'
        ]
        
        missing = []
        for file_pattern in required_files:
            if '*' in file_pattern:
                if not list(self.path.glob(file_pattern)):
                    missing.append(file_pattern)
            else:
                if not (self.path / file_pattern).exists():
                    missing.append(file_pattern)
        
        return missing
    
    def extract_key_metrics(self):
        """Extrai métricas chave para os gráficos finais"""
        try:
            with open(self.path / 'final_report.json', 'r') as f:
                report = json.load(f)
            
            # Extrair dados estruturados
            metrics = {
                'experiment': {
                    'categoria': self.categoria,
                    'problema': self.problema,
                    'data': datetime.now().isoformat()
                },
                'fatores': {
                    'ajuste_mediano': report.get('calibration_analysis', {}).get('adjustment_factor', 0),
                    'ajuste_iqr': 0,  # Calcular do relatório
                    'confiabilidade': 'Alta' if report.get('calibration_analysis', {}).get('reliable', False) else 'Baixa'
                },
                'validacao': {
                    'cses_real': 0,  # Extrair dos metadados
                    'nosso_benchmark': 0,  # Calcular
                    'correlacao': 0
                },
                'seletividade': {
                    'preservada': report.get('slow_solution_validation', {}).get('overall_selectivity', {}).get('preserved', False)
                }
            }
            
            return metrics
            
        except Exception as e:
            print(f"❌ Erro ao extrair métricas: {e}")
            return None
    
    def generate_checklist(self):
        """Gera checklist interativo"""
        print(f"\n🔍 CHECKLIST - {self.categoria.upper()}/{self.problema}")
        print("=" * 60)
        
        # 1. Arquivos obrigatórios
        print("\n📁 1. ARQUIVOS OBRIGATÓRIOS:")
        missing = self.check_required_files()
        if not missing:
            print("   ✅ Todos os arquivos necessários estão presentes")
        else:
            print(f"   ❌ Arquivos faltando: {missing}")
            return False
        
        # 2. Métricas chave
        print("\n📊 2. MÉTRICAS PARA GRÁFICOS:")
        metrics = self.extract_key_metrics()
        if metrics:
            print(f"   ✅ Fator de ajuste: {metrics['fatores']['ajuste_mediano']:.2f}x")
            print(f"   ✅ Confiabilidade: {metrics['fatores']['confiabilidade']}")
            print(f"   ✅ Seletividade preservada: {metrics['seletividade']['preservada']}")
        else:
            print("   ❌ Erro ao extrair métricas")
            return False
        
        # 3. Checklist manual
        print("\n✋ 3. VERIFICAÇÃO MANUAL:")
        manual_checks = [
            "Fator de ajuste é realista (< 50x)?",
            "Pelo menos 3 tamanhos de input testados?",
            "Slow solutions deram TLE em ambos sistemas?",
            "Correlação com plataforma real verificada?",
            "Insights específicos documentados?",
            "Anomalias identificadas e explicadas?"
        ]
        
        all_ok = True
        for check in manual_checks:
            response = input(f"   {check} [y/N]: ").strip().lower()
            if response != 'y':
                all_ok = False
                print(f"   ⚠️  Pendente: {check}")
        
        # 4. Classificação para gráficos
        print("\n🎯 4. CLASSIFICAÇÃO PARA ANÁLISE FINAL:")
        
        emblemático = input("   Este caso é emblemático da categoria? [y/N]: ").strip().lower() == 'y'
        representa_bem = input("   Representa bem o comportamento típico? [y/N]: ").strip().lower() == 'y'
        dados_suficientes = input("   Dados suficientes para generalização? [y/N]: ").strip().lower() == 'y'
        
        if emblemático and representa_bem and dados_suficientes:
            prioridade = "Alta"
        elif representa_bem and dados_suficientes:
            prioridade = "Média"
        else:
            prioridade = "Baixa"
        
        print(f"   🏆 Prioridade para gráficos finais: {prioridade}")
        
        # 5. Salvar metadados
        metadata = {
            **metrics,
            'qualidade': {
                'completo': all_ok,
                'emblemático': emblemático,
                'representa_categoria': representa_bem,
                'dados_suficientes': dados_suficientes,
                'prioridade_graficos': prioridade
            },
            'timestamp_checklist': datetime.now().isoformat()
        }
        
        output_file = self.path / 'metadata_graficos.json'
        with open(output_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n💾 Metadados salvos em: {output_file}")
        
        return all_ok and emblemático
    
    def generate_summary(self):
        """Gera resumo executivo do experimento"""
        try:
            with open(self.path / 'metadata_graficos.json', 'r') as f:
                meta = json.load(f)
            
            summary = f"""
# RESUMO EXECUTIVO - {self.categoria.upper()}/{self.problema}

## 🎯 RESULTADOS PRINCIPAIS
- **Fator de Ajuste**: {meta['fatores']['ajuste_mediano']:.2f}x
- **Confiabilidade**: {meta['fatores']['confiabilidade']}
- **Seletividade**: {'✅ Preservada' if meta['seletividade']['preservada'] else '❌ Comprometida'}

## 📊 CLASSIFICAÇÃO
- **Prioridade Gráficos**: {meta['qualidade']['prioridade_graficos']}
- **Emblemático**: {'✅' if meta['qualidade']['emblemático'] else '❌'}
- **Representa Categoria**: {'✅' if meta['qualidade']['representa_categoria'] else '❌'}

## 🔗 PARA ANÁLISE FINAL
- [ ] Incluir no gráfico executivo de fatores
- [ ] {'✅' if meta['qualidade']['emblemático'] else '❌'} Caso narrativo individual
- [ ] Incluir no heatmap de injustiça
- [ ] Incluir na validação externa

---
Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            with open(self.path / 'RESUMO_EXECUTIVO.md', 'w') as f:
                f.write(summary)
            
            print("📋 Resumo executivo gerado!")
            
        except Exception as e:
            print(f"❌ Erro ao gerar resumo: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Uso: python CHECKLIST_EXPERIMENTO.py <caminho_do_experimento>")
        sys.exit(1)
    
    experiment_path = sys.argv[1]
    checker = ExperimentChecklist(experiment_path)
    
    print("🚀 INICIANDO CHECKLIST PÓS-EXPERIMENTO")
    
    if checker.generate_checklist():
        checker.generate_summary()
        print("\n🎉 EXPERIMENTO VALIDADO E PRONTO PARA ANÁLISE FINAL!")
    else:
        print("\n⚠️  EXPERIMENTO PRECISA DE AJUSTES ANTES DA ANÁLISE FINAL")

