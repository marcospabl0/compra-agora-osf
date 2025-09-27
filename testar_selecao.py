#!/usr/bin/env python3
"""
Script para testar a nova lógica de seleção de produtos para melhoria.
Mostra quais produtos serão melhorados e por quê.
"""

import pandas as pd
from product_description_enhancer import ProductDescriptionEnhancer, OpenAIProvider

def testar_selecao_produtos():
    """Testa a seleção de produtos sem executar a melhoria."""
    
    # Ler a planilha
    print("📊 Lendo planilha de entrada...")
    df = pd.read_excel('entrada_descricao.xlsx')
    print(f"✅ Total de produtos: {len(df)}")
    
    # Criar um provedor dummy (não será usado)
    class DummyProvider:
        def enhance_description(self, product):
            return "DESCRIÇÃO_MELHORADA_TESTE"
    
    # Criar melhorador
    enhancer = ProductDescriptionEnhancer(DummyProvider(), min_description_ratio=1.5)
    
    # Analisar cada produto
    produtos_melhorar = []
    produtos_manter = []
    
    print("\n🔍 Analisando produtos...")
    print("=" * 80)
    
    for index, row in df.iterrows():
        title = str(row.get('Título', '')).strip()
        description = str(row.get('Descrição', '')).strip()
        
        should_enhance, motivo = enhancer.should_enhance_description(title, description)
        
        if should_enhance:
            produtos_melhorar.append({
                'index': index,
                'title': title,
                'description': description,
                'motivo': motivo
            })
        else:
            produtos_manter.append({
                'index': index,
                'title': title,
                'description': description,
                'motivo': motivo
            })
    
    # Mostrar resultados
    print(f"\n📈 RESULTADOS DA ANÁLISE:")
    print(f"✅ Produtos que SERÃO melhorados: {len(produtos_melhorar)}")
    print(f"⏸️  Produtos que NÃO serão melhorados: {len(produtos_manter)}")
    print(f"📊 Percentual de melhoria: {(len(produtos_melhorar) / len(df) * 100):.1f}%")
    
    # Mostrar produtos que serão melhorados
    if produtos_melhorar:
        print(f"\n🔴 PRODUTOS QUE SERÃO MELHORADOS ({len(produtos_melhorar)}):")
        print("-" * 80)
        for i, produto in enumerate(produtos_melhorar[:10], 1):  # Mostrar apenas os primeiros 10
            print(f"{i:2d}. {produto['title'][:60]}...")
            print(f"    Descrição: {produto['description'][:60]}...")
            print(f"    Motivo: {produto['motivo']}")
            print()
        
        if len(produtos_melhorar) > 10:
            print(f"... e mais {len(produtos_melhorar) - 10} produtos")
    
    # Mostrar alguns produtos que não serão melhorados
    if produtos_manter:
        print(f"\n🟢 EXEMPLOS DE PRODUTOS QUE NÃO SERÃO MELHORADOS:")
        print("-" * 80)
        for i, produto in enumerate(produtos_manter[:5], 1):  # Mostrar apenas os primeiros 5
            print(f"{i}. {produto['title'][:60]}...")
            print(f"   Descrição: {produto['description'][:60]}...")
            print(f"   Motivo: {produto['motivo']}")
            print()
    
    # Estatísticas por motivo
    print(f"\n📊 ESTATÍSTICAS POR MOTIVO:")
    print("-" * 50)
    motivos = {}
    for produto in produtos_melhorar:
        motivo = produto['motivo']
        motivos[motivo] = motivos.get(motivo, 0) + 1
    
    for motivo, count in sorted(motivos.items(), key=lambda x: x[1], reverse=True):
        print(f"{motivo}: {count} produtos")
    
    return produtos_melhorar, produtos_manter

def executar_melhoria_selecionada():
    """Executa a melhoria apenas nos produtos selecionados."""
    
    resposta = input(f"\n🤔 Deseja executar a melhoria nos produtos selecionados? (s/n): ").lower().strip()
    
    if resposta in ['s', 'sim', 'y', 'yes']:
        print("\n🚀 Executando melhoria...")
        
        # Importar e configurar OpenAI
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            print("❌ OPENAI_API_KEY não encontrada no arquivo .env")
            return
        
        # Criar provedor OpenAI
        ai_provider = OpenAIProvider(api_key, model="gpt-3.5-turbo")
        
        # Criar melhorador
        enhancer = ProductDescriptionEnhancer(ai_provider, min_description_ratio=1.5)
        
        # Processar arquivo
        enhancer.process_excel_file('entrada_descricao.xlsx', 'entrada_descricao_melhorada.xlsx')
        
        print("✅ Processamento concluído!")
        print("📁 Arquivo de saída: entrada_descricao_melhorada.xlsx")
    else:
        print("⏸️ Execução cancelada.")

if __name__ == "__main__":
    print("🔧 TESTE DA NOVA LÓGICA DE SELEÇÃO")
    print("=" * 50)
    
    produtos_melhorar, produtos_manter = testar_selecao_produtos()
    
    executar_melhoria_selecionada() 