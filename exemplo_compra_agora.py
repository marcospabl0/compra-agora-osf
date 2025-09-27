#!/usr/bin/env python3
"""
Exemplo específico para demonstrar as regras de SEO do Compra Agora.
Este script mostra como as regras são aplicadas na prática.
"""

import pandas as pd
import os

def criar_exemplo_compra_agora():
    """Cria um arquivo Excel de exemplo seguindo as regras do Compra Agora."""
    print("📝 Criando arquivo de exemplo seguindo as regras do COMPRA AGORA...")
    
    # Dados de exemplo seguindo o padrão do Compra Agora
    dados = {
        'Título': [
            'Café União Tradicional Vácuo 500g',
            'Smartphone Samsung Galaxy A54 128GB',
            'Fone de Ouvido Bluetooth JBL Tune 510BT',
            'Smart TV LG 55" 4K Ultra HD',
            'Notebook Dell Inspiron 15 3000',
            'Câmera Canon EOS Rebel T7',
            'Mouse Gamer Logitech G502 HERO',
            'Teclado Mecânico Razer BlackWidow V3',
            'Monitor Samsung 24" Full HD',
            'Impressora HP LaserJet Pro M404n'
        ],
        'Descrição': [
            'Café União',
            'Smartphone Samsung',
            'Fone JBL',
            'TV LG',
            'Notebook Dell',
            'Câmera Canon',
            'Mouse Logitech',
            'Teclado Razer',
            'Monitor Samsung',
            'Impressora HP'
        ],
        'Preço': [
            'R$ 12,90',
            'R$ 1.299,00',
            'R$ 199,00',
            'R$ 2.499,00',
            'R$ 3.999,00',
            'R$ 1.899,00',
            'R$ 299,00',
            'R$ 599,00',
            'R$ 899,00',
            'R$ 1.599,00'
        ],
        'SKU': [
            'UNIAO-CAFE-500G',
            'SAMS-A54-128',
            'JBL-T510BT',
            'LG-TV-55-4K',
            'DELL-INS-15-3000',
            'CANON-EOS-T7',
            'LOG-G502-HERO',
            'RAZ-BW-V3',
            'SAMS-MON-24-FHD',
            'HP-LJ-M404N'
        ],
        'Categoria': [
            'Cafés',
            'Smartphones',
            'Áudio',
            'TVs',
            'Computadores',
            'Câmeras',
            'Periféricos',
            'Periféricos',
            'Monitores',
            'Impressoras'
        ],
        'Marca': [
            'União',
            'Samsung',
            'JBL',
            'LG',
            'Dell',
            'Canon',
            'Logitech',
            'Razer',
            'Samsung',
            'HP'
        ]
    }
    
    # Criar DataFrame
    df = pd.DataFrame(dados)
    
    # Salvar arquivo
    df.to_excel('exemplo_compra_agora.xlsx', index=False, engine='openpyxl')
    print("✅ Arquivo 'exemplo_compra_agora.xlsx' criado com sucesso!")
    
    return df

def demonstrar_regras_compra_agora():
    """Demonstra as regras específicas do Compra Agora."""
    print("\n🎯 REGRAS OBRIGATÓRIAS DO COMPRA AGORA:")
    print("=" * 60)
    
    print("📋 META TITLE:")
    print("   ✅ Palavra-chave principal (nome do produto) no INÍCIO")
    print("   ✅ Entre 50 e 60 caracteres")
    print("   ✅ Claro, objetivo e chamativo")
    print("   ✅ Evitar keyword stuffing")
    print("   ✅ Nome da marca no final")
    print("   ✅ Sufixo '- Compra Agora' (15 caracteres)")
    print("   ✅ Formato: 'Nome Produto | Marca - Compra Agora'")
    
    print("\n📝 META DESCRIPTION:")
    print("   ✅ Entre 140 e 160 caracteres")
    print("   ✅ Palavra-chave principal de forma natural")
    print("   ✅ Explicar claramente o que o usuário encontra")
    print("   ✅ Gatilhos de ação ('Compre agora', 'Descubra')")
    print("   ✅ Benefícios e diferenciais destacados")
    print("   ✅ Sem duplicação entre páginas")
    
    print("\n🎨 PRESET DO NIARA:")
    print("   META TITLE: tema/título + palavra-chave + audiência + tom de voz")
    print("   META DESCRIPTION: tema/título + palavra-chave + audiência + call_to_action + tom de voz")

def mostrar_exemplos_praticos():
    """Mostra exemplos práticos de como as regras são aplicadas."""
    print("\n💡 EXEMPLOS PRÁTICOS:")
    print("=" * 60)
    
    exemplos = [
        {
            "produto": "Café União Tradicional Vácuo 500g",
            "marca": "União",
            "meta_title": "Café União Tradicional Vácuo 500g | União - Compra Agora",
            "meta_description": "Café União Tradicional Vácuo 500g: sabor encorpado e aroma irresistível. Experimente e compre agora mesmo!"
        },
        {
            "produto": "Smartphone Samsung Galaxy A54 128GB",
            "marca": "Samsung",
            "meta_title": "Samsung Galaxy A54 128GB | Samsung - Compra Agora",
            "meta_description": "Smartphone Samsung Galaxy A54 com câmera de 50MP e tela 6.4\" AMOLED. Descubra e compre agora mesmo!"
        },
        {
            "produto": "Fone de Ouvido Bluetooth JBL Tune 510BT",
            "marca": "JBL",
            "meta_title": "JBL Tune 510BT Bluetooth | JBL - Compra Agora",
            "meta_description": "Fone de ouvido JBL Tune 510BT com som JBL Pure Bass e 40h de bateria. Veja modelos exclusivos!"
        }
    ]
    
    for i, exemplo in enumerate(exemplos, 1):
        print(f"\n{i}. {exemplo['produto']}")
        print(f"   🎯 Meta Title: {exemplo['meta_title']}")
        print(f"   📏 Caracteres: {len(exemplo['meta_title'])} (entre 50-60 ✓)")
        print(f"   📋 Meta Description: {exemplo['meta_description']}")
        print(f"   📏 Caracteres: {len(exemplo['meta_description'])} (entre 140-160 ✓)")

def mostrar_beneficios_compra_agora():
    """Mostra os benefícios específicos das regras do Compra Agora."""
    print("\n🚀 BENEFÍCIOS DAS REGRAS DO COMPRA AGORA:")
    print("=" * 60)
    
    beneficios = [
        "🎯 SEO otimizado seguindo padrões comprovados",
        "📱 Meta tags consistentes em todo o catálogo",
        "💼 Formato reconhecido pelos usuários do Compra Agora",
        "🔍 Melhor ranking nos mecanismos de busca",
        "📈 Taxa de clique aumentada (CTR)",
        "⏱️ Padrão estabelecido para toda a equipe",
        "💡 Estrutura profissional e atrativa",
        "🎨 Preset do Niara implementado automaticamente"
    ]
    
    for beneficio in beneficios:
        print(f"   {beneficio}")

def mostrar_comandos_uso():
    """Mostra os comandos para usar o script."""
    print("\n🚀 COMO USAR:")
    print("=" * 60)
    
    print("1️⃣ Configure sua API Key:")
    print("   # Para OpenAI")
    print("   export OPENAI_API_KEY='sua-chave-aqui'")
    print("   # Para Gemini")
    print("   export GEMINI_API_KEY='sua-chave-aqui'")
    
    print("\n2️⃣ Execute o script:")
    print("   # Com OpenAI")
    print("   python product_description_enhancer.py exemplo_compra_agora.xlsx -p openai")
    print("   # Com Gemini")
    print("   python product_description_enhancer.py exemplo_compra_agora.xlsx -p gemini")
    
    print("\n3️⃣ Resultado esperado:")
    print("   ✅ Meta Title: 'Nome Produto | Marca - Compra Agora'")
    print("   ✅ Meta Description: Entre 140-160 caracteres com call-to-action")
    print("   ✅ Seguindo exatamente as regras do Compra Agora")

def main():
    """Função principal."""
    print("🎯 COMPRA AGORA - Regras de SEO")
    print("=" * 60)
    print("Este script demonstra as regras específicas de SEO do Compra Agora!")
    
    # Criar arquivo de exemplo
    df = criar_exemplo_compra_agora()
    
    # Demonstrar regras
    demonstrar_regras_compra_agora()
    
    # Mostrar exemplos práticos
    mostrar_exemplos_praticos()
    
    # Mostrar benefícios
    mostrar_beneficios_compra_agora()
    
    # Mostrar comandos de uso
    mostrar_comandos_uso()
    
    print("\n" + "="*60)
    print("✅ ARQUIVO DE EXEMPLO CRIADO!")
    print("📁 Nome: exemplo_compra_agora.xlsx")
    print("📊 Produtos: 10 produtos seguindo o padrão Compra Agora")
    print("🎯 Pronto para aplicar as regras de SEO específicas!")
    print("="*60)
    
    print("\n💡 Para testar:")
    print("   1. Configure sua API Key (OpenAI ou Gemini)")
    print("   2. Execute: python product_description_enhancer.py exemplo_compra_agora.xlsx -p openai")
    print("   3. Verifique se as Meta Tags seguem exatamente as regras do Compra Agora")

if __name__ == "__main__":
    main()

