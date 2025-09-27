#!/usr/bin/env python3
"""
Exemplo de uso do melhorador de descrições de produtos.
Este script demonstra como usar o ProductDescriptionEnhancer.
"""

import pandas as pd
import os
from product_description_enhancer import ProductDescriptionEnhancer, OpenAIProvider, GeminiProvider

def criar_catalogo_exemplo():
    """Cria um catálogo de exemplo para teste."""
    
    # Dados de exemplo com produtos que têm descrições curtas
    dados = {
        'Título': [
            'Smartphone Samsung Galaxy A54 5G 128GB Preto',
            'Notebook Dell Inspiron 15 3000 Intel Core i5',
            'Smart TV LG 55" 4K UHD LED',
            'Fone de Ouvido Bluetooth JBL Tune 500BT',
            'Câmera Digital Canon EOS Rebel T7',
            'Console PlayStation 5 825GB',
            'Tablet Apple iPad 10.2" 64GB Wi-Fi',
            'Smartwatch Samsung Galaxy Watch 5',
            'Drone DJI Mini 2 Fly More Combo',
            'Impressora HP LaserJet Pro M404n'
        ],
        'Descrição': [
            'Smartphone Samsung',
            'Notebook Dell',
            'Smart TV LG',
            'Fone JBL',
            'Câmera Canon',
            'PlayStation 5',
            'iPad Apple',
            'Smartwatch Samsung',
            'Drone DJI',
            'Impressora HP'
        ],
        'Preço': [
            'R$ 1.999,00',
            'R$ 3.499,00',
            'R$ 2.799,00',
            'R$ 299,00',
            'R$ 2.199,00',
            'R$ 3.999,00',
            'R$ 2.899,00',
            'R$ 1.499,00',
            'R$ 2.999,00',
            'R$ 899,00'
        ],
        'SKU': [
            'SAMS-A54-128-PRETO',
            'DELL-INSP-15-I5',
            'LG-TV-55-4K',
            'JBL-TUNE-500BT',
            'CANON-EOS-T7',
            'SONY-PS5-825GB',
            'APPLE-IPAD-10-64GB',
            'SAMS-GW5-44MM',
            'DJI-MINI2-FLYMORE',
            'HP-LASERJET-M404N'
        ],
        'Categoria': [
            'Smartphones',
            'Notebooks',
            'TVs',
            'Áudio',
            'Câmeras',
            'Games',
            'Tablets',
            'Smartwatches',
            'Drones',
            'Impressoras'
        ],
        'Marca': [
            'Samsung',
            'Dell',
            'LG',
            'JBL',
            'Canon',
            'Sony',
            'Apple',
            'Samsung',
            'DJI',
            'HP'
        ]
    }
    
    df = pd.DataFrame(dados)
    df.to_excel('catalogo_exemplo.xlsx', index=False)
    print("Catálogo de exemplo criado: catalogo_exemplo.xlsx")
    print(f"Total de produtos: {len(df)}")
    print("Produtos com descrições curtas que serão melhoradas:")

def analisar_descricoes():
    """Analisa as descrições do catálogo de exemplo."""
    
    try:
        df = pd.read_excel('catalogo_exemplo.xlsx')
        
        print("\n=== Análise das Descrições ===")
        for index, row in df.iterrows():
            title = row['Título']
            description = row['Descrição']
            
            title_length = len(title)
            description_length = len(description)
            ratio = description_length / title_length if title_length > 0 else 0
            
            status = "MELHORAR" if ratio < 1.5 else "OK"
            
            print(f"{index + 1}. {title[:40]}...")
            print(f"   Descrição: {description}")
            print(f"   Razão: {ratio:.2f} ({status})")
            print()
            
    except FileNotFoundError:
        print("Arquivo 'catalogo_exemplo.xlsx' não encontrado. Execute primeiro criar_catalogo_exemplo()")

def exemplo_uso_openai():
    """Demonstra uso com OpenAI (requer API key)."""
    
    print("=== Exemplo com OpenAI ===")
    
    # Verificar se há API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  OPENAI_API_KEY não configurada. Configure a variável de ambiente ou use -k")
        print("   export OPENAI_API_KEY='sua-chave-aqui'")
        return
    
    try:
        # Criar provedor OpenAI
        ai_provider = OpenAIProvider(api_key, "gpt-3.5-turbo")
        
        # Criar melhorador
        enhancer = ProductDescriptionEnhancer(ai_provider, min_description_ratio=1.5)
        
        # Processar arquivo
        enhancer.process_excel_file('catalogo_exemplo.xlsx', 'catalogo_melhorado_openai.xlsx')
        
        print("✅ Processamento com OpenAI concluído!")
        print("📁 Arquivo gerado: catalogo_melhorado_openai.xlsx")
        
    except Exception as e:
        print(f"❌ Erro ao usar OpenAI: {str(e)}")

def exemplo_uso_gemini():
    """Demonstra uso com Gemini (requer API key)."""
    
    print("=== Exemplo com Gemini ===")
    
    # Verificar se há API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("⚠️  GEMINI_API_KEY não configurada. Configure a variável de ambiente ou use -k")
        print("   export GEMINI_API_KEY='sua-chave-aqui'")
        return
    
    try:
        # Criar provedor Gemini
        ai_provider = GeminiProvider(api_key, "gemini-pro")
        
        # Criar melhorador
        enhancer = ProductDescriptionEnhancer(ai_provider, min_description_ratio=1.5)
        
        # Processar arquivo
        enhancer.process_excel_file('catalogo_exemplo.xlsx', 'catalogo_melhorado_gemini.xlsx')
        
        print("✅ Processamento com Gemini concluído!")
        print("📁 Arquivo gerado: catalogo_melhorado_gemini.xlsx")
        
    except Exception as e:
        print(f"❌ Erro ao usar Gemini: {str(e)}")

def mostrar_estrutura_arquivo():
    """Mostra a estrutura esperada do arquivo Excel."""
    
    print("=== Estrutura Esperada do Arquivo Excel ===")
    print("""
Colunas obrigatórias:
- Título: Nome/título do produto
- Descrição: Descrição atual do produto

Colunas opcionais:
- Preço: Preço do produto
- SKU: Código SKU do produto
- Categoria: Categoria do produto
- Marca: Marca do produto

Exemplo de estrutura:
| Título | Descrição | Preço | SKU | Categoria | Marca |
|--------|-----------|-------|-----|-----------|-------|
| Smartphone Samsung Galaxy A54 | Smartphone Samsung | R$ 1.999,00 | SAMS-A54 | Smartphones | Samsung |
""")

def instrucoes_configuracao():
    """Mostra instruções de configuração."""
    
    print("=== Instruções de Configuração ===")
    print("""
1. Configure sua API Key:

   Para OpenAI:
   export OPENAI_API_KEY='sk-...'
   
   Para Gemini:
   export GEMINI_API_KEY='AIza...'

2. Execute o script:
   python product_description_enhancer.py catalogo_exemplo.xlsx -p openai
   python product_description_enhancer.py catalogo_exemplo.xlsx -p gemini

3. Opções disponíveis:
   -p, --provider: openai ou gemini
   -k, --api-key: chave da API
   -r, --ratio: razão mínima descrição/título (padrão: 1.5)
   -o, --output: arquivo de saída
   -m, --model: modelo específico
""")

if __name__ == "__main__":
    print("=== Exemplo de Uso do Melhorador de Descrições ===\n")
    
    # Mostrar estrutura esperada
    mostrar_estrutura_arquivo()
    
    # Criar catálogo de exemplo
    print("1. Criando catálogo de exemplo...")
    criar_catalogo_exemplo()
    print()
    
    # Analisar descrições
    print("2. Analisando descrições...")
    analisar_descricoes()
    print()
    
    # Mostrar instruções
    print("3. Instruções de configuração:")
    instrucoes_configuracao()
    print()
    
    # Exemplos com APIs (se configuradas)
    print("4. Exemplos de uso:")
    exemplo_uso_openai()
    print()
    exemplo_uso_gemini()
    print()
    
    print("=== Exemplo concluído! ===")
    print("Arquivos gerados:")
    print("- catalogo_exemplo.xlsx (catálogo de exemplo)")
    print("- product_enhancer.log (logs do processo)")
    print("\nPara usar com suas próprias APIs:")
    print("1. Configure as variáveis de ambiente com suas API keys")
    print("2. Execute: python product_description_enhancer.py seu_catalogo.xlsx") 