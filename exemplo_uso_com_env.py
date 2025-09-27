#!/usr/bin/env python3
"""
Exemplo de uso do melhorador de descrições com arquivo .env
Este script demonstra como usar o ProductDescriptionEnhancer com API key do arquivo .env
"""

import pandas as pd
import os
from dotenv import load_dotenv
from product_description_enhancer import ProductDescriptionEnhancer, OpenAIProvider

def criar_catalogo_teste():
    """Cria um catálogo de teste com produtos que têm descrições curtas."""
    
    dados = {
        'Título': [
            'Smartphone Samsung Galaxy A54 5G 128GB Preto',
            'Notebook Dell Inspiron 15 3000 Intel Core i5 8GB 256GB SSD',
            'Smart TV LG 55" 4K UHD LED WebOS',
            'Fone de Ouvido Bluetooth JBL Tune 500BT Preto',
            'Câmera Digital Canon EOS Rebel T7 24.1MP'
        ],
        'Descrição': [
            'Smartphone Samsung',
            'Notebook Dell',
            'Smart TV LG',
            'Fone JBL',
            'Câmera Canon'
        ],
        'Preço': [
            'R$ 1.999,00',
            'R$ 3.499,00',
            'R$ 2.799,00',
            'R$ 299,00',
            'R$ 2.199,00'
        ],
        'SKU': [
            'SAMS-A54-128-PRETO',
            'DELL-INSP-15-I5',
            'LG-TV-55-4K',
            'JBL-TUNE-500BT',
            'CANON-EOS-T7'
        ],
        'Categoria': [
            'Smartphones',
            'Notebooks',
            'TVs',
            'Áudio',
            'Câmeras'
        ],
        'Marca': [
            'Samsung',
            'Dell',
            'LG',
            'JBL',
            'Canon'
        ]
    }
    
    df = pd.DataFrame(dados)
    df.to_excel('catalogo_teste.xlsx', index=False)
    print("✅ Catálogo de teste criado: catalogo_teste.xlsx")
    return df

def verificar_configuracao():
    """Verifica se a configuração está correta."""
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Verificar API key
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("✅ OPENAI_API_KEY encontrada no arquivo .env")
        print(f"   Chave: {api_key[:20]}...{api_key[-10:]}")
    else:
        print("❌ OPENAI_API_KEY não encontrada no arquivo .env")
        return False
    
    # Verificar dependências
    try:
        import pandas
        import openai
        import openpyxl
        print("✅ Todas as dependências estão instaladas")
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        return False
    
    return True

def executar_melhoria():
    """Executa a melhoria de descrições usando o arquivo .env."""
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Obter API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY não encontrada")
        return
    
    # Criar provedor OpenAI
    ai_provider = OpenAIProvider(api_key, model="gpt-3.5-turbo")
    
    # Criar melhorador
    enhancer = ProductDescriptionEnhancer(ai_provider, min_description_ratio=1.5)
    
    # Processar arquivo
    print("🚀 Iniciando melhoria de descrições...")
    enhancer.process_excel_file('catalogo_teste.xlsx', 'catalogo_teste_melhorado.xlsx')
    
    print("✅ Processamento concluído!")
    print("📁 Arquivo de saída: catalogo_teste_melhorado.xlsx")

def mostrar_instrucoes():
    """Mostra instruções de uso."""
    
    print("\n" + "="*60)
    print("📖 INSTRUÇÕES DE USO")
    print("="*60)
    print("1. ✅ Arquivo .env criado com sua API key")
    print("2. ✅ Dependências instaladas")
    print("3. ✅ Script configurado para usar variáveis de ambiente")
    print("\n🚀 COMO USAR:")
    print("   python product_description_enhancer.py sua_planilha.xlsx -p openai")
    print("\n📋 FORMATO DA PLANILHA:")
    print("   - Colunas obrigatórias: Título, Descrição")
    print("   - Colunas opcionais: Preço, SKU, Categoria, Marca")
    print("\n🔒 SEGURANÇA:")
    print("   - Arquivo .env está no .gitignore (não será commitado)")
    print("   - API key é carregada automaticamente do arquivo .env")

def main():
    """Função principal."""
    
    print("🔧 CONFIGURAÇÃO DO SISTEMA")
    print("="*40)
    
    # Verificar configuração
    if not verificar_configuracao():
        print("❌ Configuração incompleta. Verifique as dependências e o arquivo .env")
        return
    
    # Criar catálogo de teste
    print("\n📊 CRIANDO CATÁLOGO DE TESTE")
    print("-" * 30)
    df = criar_catalogo_teste()
    
    # Mostrar produtos que serão melhorados
    print("\n📋 PRODUTOS QUE SERÃO MELHORADOS:")
    print("-" * 40)
    for i, (titulo, descricao) in enumerate(zip(df['Título'], df['Descrição']), 1):
        razao = len(descricao) / len(titulo)
        status = "🔴 MELHORAR" if razao < 1.5 else "🟢 MANTER"
        print(f"{i}. {status} | Razão: {razao:.2f} | {titulo[:40]}...")
    
    # Perguntar se quer executar
    print("\n" + "="*50)
    resposta = input("🤔 Deseja executar a melhoria agora? (s/n): ").lower().strip()
    
    if resposta in ['s', 'sim', 'y', 'yes']:
        print("\n🚀 EXECUTANDO MELHORIA...")
        print("-" * 25)
        executar_melhoria()
    else:
        print("\n⏸️  Execução cancelada.")
        print("💡 Para executar depois, use:")
        print("   python product_description_enhancer.py catalogo_teste.xlsx -p openai")
    
    # Mostrar instruções
    mostrar_instrucoes()

if __name__ == "__main__":
    main() 