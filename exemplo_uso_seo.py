#!/usr/bin/env python3
"""
Exemplo de uso do script melhorador de produtos com funcionalidades de SEO.
Este script demonstra como gerar Meta Title e Meta Description para produtos.
"""

import os
import pandas as pd
from product_description_enhancer import ProductDescriptionEnhancer, OpenAIProvider, GeminiProvider

def exemplo_openai():
    """Exemplo usando OpenAI para gerar conteúdo SEO."""
    print("🚀 Exemplo usando OpenAI GPT")
    print("=" * 50)
    
    # Configurar API Key (ou usar variável de ambiente)
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Configure a variável de ambiente OPENAI_API_KEY")
        return
    
    # Criar provedor OpenAI
    ai_provider = OpenAIProvider(api_key, model="gpt-3.5-turbo")
    
    # Criar melhorador
    enhancer = ProductDescriptionEnhancer(ai_provider, min_ratio=1.5)
    
    # Processar arquivo
    input_file = "entrada_descricao.xlsx"
    output_file = "saida_com_seo.xlsx"
    
    if os.path.exists(input_file):
        print(f"📁 Processando arquivo: {input_file}")
        enhancer.process_excel_file(input_file, output_file)
        print(f"✅ Arquivo processado salvo como: {output_file}")
    else:
        print(f"❌ Arquivo {input_file} não encontrado")

def exemplo_gemini():
    """Exemplo usando Google Gemini para gerar conteúdo SEO."""
    print("\n🚀 Exemplo usando Google Gemini")
    print("=" * 50)
    
    # Configurar API Key (ou usar variável de ambiente)
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Configure a variável de ambiente GEMINI_API_KEY")
        return
    
    # Criar provedor Gemini
    ai_provider = GeminiProvider(api_key, model="gemini-pro")
    
    # Criar melhorador
    enhancer = ProductDescriptionEnhancer(ai_provider, min_ratio=1.5)
    
    # Processar arquivo
    input_file = "entrada_descricao.xlsx"
    output_file = "saida_com_seo_gemini.xlsx"
    
    if os.path.exists(input_file):
        print(f"📁 Processando arquivo: {input_file}")
        enhancer.process_excel_file(input_file, output_file)
        print(f"✅ Arquivo processado salvo como: {output_file}")
    else:
        print(f"❌ Arquivo {input_file} não encontrado")

def criar_arquivo_exemplo():
    """Cria um arquivo Excel de exemplo para teste."""
    print("\n📝 Criando arquivo de exemplo...")
    
    # Dados de exemplo
    dados = {
        'Título': [
            'Smartphone Samsung Galaxy A54',
            'Fone de Ouvido Bluetooth JBL',
            'Smart TV LG 55" 4K',
            'Notebook Dell Inspiron 15',
            'Câmera Canon EOS Rebel'
        ],
        'Descrição': [
            'Smartphone Samsung',
            'Fone JBL',
            'TV LG',
            'Notebook Dell',
            'Câmera Canon'
        ],
        'Preço': [
            'R$ 1.299,00',
            'R$ 199,00',
            'R$ 2.499,00',
            'R$ 3.999,00',
            'R$ 1.899,00'
        ],
        'SKU': [
            'SAMS-A54-128',
            'JBL-BT-001',
            'LG-TV-55-4K',
            'DELL-INS-15',
            'CANON-EOS-R'
        ],
        'Categoria': [
            'Smartphones',
            'Áudio',
            'TVs',
            'Computadores',
            'Câmeras'
        ],
        'Marca': [
            'Samsung',
            'JBL',
            'LG',
            'Dell',
            'Canon'
        ]
    }
    
    # Criar DataFrame
    df = pd.DataFrame(dados)
    
    # Salvar arquivo
    df.to_excel('entrada_descricao.xlsx', index=False, engine='openpyxl')
    print("✅ Arquivo 'entrada_descricao.xlsx' criado com sucesso!")

def mostrar_colunas_saida():
    """Mostra as colunas que serão geradas na saída."""
    print("\n📊 Colunas de saída do script:")
    print("=" * 50)
    
    colunas = [
        "Título (original)",
        "Descrição (original)", 
        "Preço (original)",
        "SKU (original)",
        "Categoria (original)",
        "Marca (original)",
        "Descrição_Melhorada (nova)",
        "Status_Melhoria (nova)",
        "Motivo_Melhoria (nova)",
        "Razão_Título_Descrição (nova)",
        "Meta_Title (nova) 🎯",
        "Meta_Description (nova) 📋"
    ]
    
    for i, coluna in enumerate(colunas, 1):
        if "nova" in coluna:
            print(f"{i:2d}. {coluna}")
        else:
            print(f"{i:2d}. {coluna}")
    
    print("\n✨ Novas funcionalidades:")
    print("   🎯 Meta Title: Título otimizado para SEO (máx. 60 caracteres)")
    print("   📋 Meta Description: Descrição para resultados de busca (máx. 160 caracteres)")
    print("   🔍 SEO otimizado: Palavras-chave e estrutura para melhor ranking")

def main():
    """Função principal."""
    print("🎯 Melhorador de Produtos com SEO")
    print("=" * 50)
    print("Este script agora gera Meta Title e Meta Description para todos os produtos!")
    
    # Criar arquivo de exemplo se não existir
    if not os.path.exists('entrada_descricao.xlsx'):
        criar_arquivo_exemplo()
    
    # Mostrar colunas de saída
    mostrar_colunas_saida()
    
    # Exemplos de uso
    print("\n" + "="*50)
    print("EXEMPLOS DE USO:")
    print("="*50)
    
    # Verificar qual API está disponível
    openai_key = os.getenv('OPENAI_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if openai_key:
        print("\n🔑 OpenAI API Key encontrada!")
        exemplo_openai()
    elif gemini_key:
        print("\n🔑 Gemini API Key encontrada!")
        exemplo_gemini()
    else:
        print("\n❌ Nenhuma API Key configurada!")
        print("Configure uma das seguintes variáveis de ambiente:")
        print("   - OPENAI_API_KEY para usar OpenAI")
        print("   - GEMINI_API_KEY para usar Google Gemini")
        print("\nOu execute via linha de comando:")
        print("   python product_description_enhancer.py entrada_descricao.xlsx -p openai")
        print("   python product_description_enhancer.py entrada_descricao.xlsx -p gemini")

if __name__ == "__main__":
    main()

