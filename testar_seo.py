#!/usr/bin/env python3
"""
Script de teste para as funcionalidades de SEO do melhorador de produtos.
Este script testa a geração de Meta Title e Meta Description sem precisar de API keys.
"""

import pandas as pd
import os
from datetime import datetime

def criar_arquivo_teste():
    """Cria um arquivo Excel de teste com produtos para demonstrar as funcionalidades."""
    print("📝 Criando arquivo de teste para demonstração das funcionalidades SEO...")
    
    # Dados de teste com diferentes cenários
    dados = {
        'Título': [
            'Smartphone Samsung Galaxy A54 128GB',
            'Fone de Ouvido Bluetooth JBL Tune 510BT',
            'Smart TV LG 55" 4K Ultra HD',
            'Notebook Dell Inspiron 15 3000',
            'Câmera Canon EOS Rebel T7',
            'Mouse Gamer Logitech G502 HERO',
            'Teclado Mecânico Razer BlackWidow V3',
            'Monitor Samsung 24" Full HD',
            'Impressora HP LaserJet Pro M404n',
            'Webcam Logitech C920 HD Pro'
        ],
        'Descrição': [
            'Smartphone Samsung',
            'Fone JBL',
            'TV LG',
            'Notebook Dell',
            'Câmera Canon',
            'Mouse Logitech',
            'Teclado Razer',
            'Monitor Samsung',
            'Impressora HP',
            'Webcam Logitech'
        ],
        'Preço': [
            'R$ 1.299,00',
            'R$ 199,00',
            'R$ 2.499,00',
            'R$ 3.999,00',
            'R$ 1.899,00',
            'R$ 299,00',
            'R$ 599,00',
            'R$ 899,00',
            'R$ 1.599,00',
            'R$ 399,00'
        ],
        'SKU': [
            'SAMS-A54-128',
            'JBL-T510BT',
            'LG-TV-55-4K',
            'DELL-INS-15-3000',
            'CANON-EOS-T7',
            'LOG-G502-HERO',
            'RAZ-BW-V3',
            'SAMS-MON-24-FHD',
            'HP-LJ-M404N',
            'LOG-C920-HD'
        ],
        'Categoria': [
            'Smartphones',
            'Áudio',
            'TVs',
            'Computadores',
            'Câmeras',
            'Periféricos',
            'Periféricos',
            'Monitores',
            'Impressoras',
            'Webcams'
        ],
        'Marca': [
            'Samsung',
            'JBL',
            'LG',
            'Dell',
            'Canon',
            'Logitech',
            'Razer',
            'Samsung',
            'HP',
            'Logitech'
        ]
    }
    
    # Criar DataFrame
    df = pd.DataFrame(dados)
    
    # Salvar arquivo
    df.to_excel('teste_seo.xlsx', index=False, engine='openpyxl')
    print("✅ Arquivo 'teste_seo.xlsx' criado com sucesso!")
    
    return df

def mostrar_estrutura_entrada():
    """Mostra a estrutura do arquivo de entrada."""
    print("\n📊 Estrutura do arquivo de entrada:")
    print("=" * 50)
    
    colunas = [
        "Título",
        "Descrição", 
        "Preço",
        "SKU",
        "Categoria",
        "Marca"
    ]
    
    for i, coluna in enumerate(colunas, 1):
        print(f"{i}. {coluna}")
    
    print("\n💡 Este arquivo será processado para gerar:")
    print("   - Descrições melhoradas (quando necessário)")
    print("   - Meta Title otimizado para SEO")
    print("   - Meta Description otimizada para SEO")

def mostrar_estrutura_saida():
    """Mostra a estrutura do arquivo de saída."""
    print("\n📊 Estrutura do arquivo de saída:")
    print("=" * 50)
    
    colunas_originais = [
        "Título (original)",
        "Descrição (original)", 
        "Preço (original)",
        "SKU (original)",
        "Categoria (original)",
        "Marca (original)"
    ]
    
    colunas_novas = [
        "Descrição_Melhorada (nova)",
        "Status_Melhoria (nova)",
        "Motivo_Melhoria (nova)",
        "Razão_Título_Descrição (nova)",
        "Meta_Title (nova) 🎯",
        "Meta_Description (nova) 📋"
    ]
    
    print("📋 Colunas originais:")
    for i, coluna in enumerate(colunas_originais, 1):
        print(f"   {i}. {coluna}")
    
    print("\n✨ Colunas geradas pelo script:")
    for i, coluna in enumerate(colunas_novas, 1):
        print(f"   {i}. {coluna}")

def demonstrar_regras_seo():
    """Demonstra as regras de SEO aplicadas seguindo o Compra Agora."""
    print("\n🔍 Regras de SEO do COMPRA AGORA:")
    print("=" * 50)
    
    print("🎯 META TITLE (Regras Obrigatórias):")
    print("   • Usar a palavra-chave principal (nome do produto) no INÍCIO sempre que possível")
    print("   • Manter entre 50 e 60 caracteres (para não cortar nos resultados)")
    print("   • Ser claro e objetivo, mas chamativo")
    print("   • Evitar repetições de palavras-chave (keyword stuffing)")
    print("   • Incluir o nome da marca no final")
    print("   • ('- Compra Agora' consome 15 caracteres)")
    print("   • Formato: 'Nome Produto | Marca - Compra Agora'")
    print("   • Exemplo: 'Café União Tradicional Vácuo | União - Compra Agora'")
    
    print("\n📋 META DESCRIPTION (Regras Obrigatórias):")
    print("   • Entre 140 e 160 caracteres (acima disso o Google corta)")
    print("   • Usar a palavra-chave principal de forma natural")
    print("   • Explicar de forma clara o que o usuário encontra na página")
    print("   • Inserir gatilhos de ação ('Compre agora', 'Descubra', 'Veja modelos exclusivos')")
    print("   • Destacar benefícios e diferenciais (ex: 'Edição limitada', 'Feito à mão')")
    print("   • Não duplicar descriptions em várias páginas")
    print("   • Exemplo: 'Café União Tradicional Vácuo 500g: sabor encorpado e aroma irresistível. Experimente e compre agora mesmo!'")
    
    print("\n🎨 PRESET DO NIARA:")
    print("   META TITLE: tema/título + palavra-chave + audiência + tom de voz")
    print("   META DESCRIPTION: tema/título + palavra-chave + audiência + call_to_action + tom de voz")
    
    print("\n💡 EXEMPLOS PRÁTICOS:")
    print("   📱 Smartphone: 'Samsung Galaxy A54 | Samsung - Compra Agora'")
    print("   🎧 Fone: 'JBL Tune 510BT | JBL - Compra Agora'")
    print("   📺 TV: 'LG 55\" 4K Ultra HD | LG - Compra Agora'")

def mostrar_comandos_uso():
    """Mostra os comandos para usar o script."""
    print("\n🚀 Como usar o script:")
    print("=" * 50)
    
    print("1️⃣ Configure sua API Key:")
    print("   # Para OpenAI")
    print("   export OPENAI_API_KEY='sua-chave-aqui'")
    print("   # Para Gemini")
    print("   export GEMINI_API_KEY='sua-chave-aqui'")
    
    print("\n2️⃣ Execute o script:")
    print("   # Com OpenAI")
    print("   python product_description_enhancer.py teste_seo.xlsx -p openai")
    print("   # Com Gemini")
    print("   python product_description_enhancer.py teste_seo.xlsx -p gemini")
    
    print("\n3️⃣ Opções disponíveis:")
    print("   -o arquivo_saida.xlsx  # Especificar arquivo de saída")
    print("   -r 2.0                 # Ajustar razão mínima")
    print("   -m gpt-4               # Usar modelo específico")

def mostrar_beneficios():
    """Mostra os benefícios das funcionalidades de SEO."""
    print("\n🚀 Benefícios das funcionalidades de SEO:")
    print("=" * 50)
    
    beneficios = [
        "🎯 Melhor ranking nos mecanismos de busca",
        "📈 Mais cliques nos resultados de busca",
        "💼 Conversões aumentadas",
        "⏱️ Tempo economizado na otimização manual",
        "🔍 SEO consistente em todo o catálogo",
        "📱 Meta tags otimizadas para cada produto",
        "💡 Palavras-chave estrategicamente posicionadas",
        "🎨 Estrutura profissional e atrativa"
    ]
    
    for beneficio in beneficios:
        print(f"   {beneficio}")

def main():
    """Função principal."""
    print("🎯 Teste das Funcionalidades de SEO")
    print("=" * 50)
    print("Este script demonstra as novas funcionalidades de Meta Title e Meta Description!")
    
    # Criar arquivo de teste
    df = criar_arquivo_teste()
    
    # Mostrar estrutura
    mostrar_estrutura_entrada()
    mostrar_estrutura_saida()
    
    # Demonstrar regras de SEO
    demonstrar_regras_seo()
    
    # Mostrar comandos de uso
    mostrar_comandos_uso()
    
    # Mostrar benefícios
    mostrar_beneficios()
    
    print("\n" + "="*50)
    print("✅ ARQUIVO DE TESTE CRIADO!")
    print("📁 Nome: teste_seo.xlsx")
    print("📊 Produtos: 10 produtos de exemplo")
    print("🎯 Pronto para testar as funcionalidades de SEO!")
    print("="*50)
    
    print("\n💡 Para testar:")
    print("   1. Configure sua API Key (OpenAI ou Gemini)")
    print("   2. Execute: python product_description_enhancer.py teste_seo.xlsx -p openai")
    print("   3. Verifique o arquivo de saída com Meta Title e Meta Description")

if __name__ == "__main__":
    main()
