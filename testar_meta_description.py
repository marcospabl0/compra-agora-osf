#!/usr/bin/env python3
"""
Script para testar e debugar o problema das Meta Descriptions com "..." no final.
Identifica quando e por que as Meta Descriptions estão sendo cortadas.
"""

from product_description_enhancer import clean_product_title, ProductInfo
import re

def test_meta_description_length():
    """Testa diferentes cenários de Meta Description para identificar o problema."""
    
    print("🔍 INVESTIGANDO META DESCRIPTIONS COM '...' NO FINAL")
    print("=" * 70)
    print("Este script identifica quando e por que as Meta Descriptions são cortadas\n")
    
    # Exemplos de produtos para teste
    test_products = [
        {
            "title": "Whisky Black & White 700mL",
            "description": "Whisky escocês tradicional com sabor suave e equilibrado",
            "brand": "Black & White",
            "category": "Bebidas"
        },
        {
            "title": "Smartphone Samsung Galaxy A54 128GB Azul",
            "description": "Smartphone Samsung com câmera de 50MP",
            "brand": "Samsung",
            "category": "Eletrônicos"
        },
        {
            "title": "Antitranspirante Dove Men+Care Invisible Dry 150ml",
            "description": "Antitranspirante com proteção duradoura",
            "brand": "Dove",
            "category": "Higiene"
        }
    ]
    
    for i, product_data in enumerate(test_products, 1):
        print(f"📱 PRODUTO {i}: {product_data['title']}")
        print("-" * 50)
        
        # Criar objeto ProductInfo
        product = ProductInfo(
            title=product_data['title'],
            description=product_data['description'],
            brand=product_data['brand'],
            category=product_data['category']
        )
        
        # Simular geração de Meta Description
        clean_title = clean_product_title(product.title)
        
        # Simular Meta Description como seria gerada pela IA
        meta_description = f"{clean_title} com {product_data['description']}. Descubra a qualidade superior deste produto e aproveite os benefícios exclusivos. Compre agora na Compra Agora e sinta a diferença!"
        
        print(f"Meta Description Simulada:")
        print(f"'{meta_description}'")
        print(f"Comprimento: {len(meta_description)} caracteres")
        
        # Verificar se seria cortada
        if len(meta_description) > 160:
            print(f"❌ EXCESSO: {len(meta_description) - 160} caracteres a mais")
            print(f"Será cortada para: {meta_description[:157]}...")
            print(f"Caracteres perdidos: {meta_description[157:]}")
        else:
            print(f"✅ OK: Dentro do limite de 160 caracteres")
        
        print()
    
    print("=" * 70)
    print("🔧 SOLUÇÕES POSSÍVEIS:")
    print("1. Otimizar prompts para gerar descrições mais concisas")
    print("2. Implementar lógica mais inteligente de corte")
    print("3. Ajustar limites de caracteres")
    print("4. Melhorar validação de comprimento")

def analyze_cutting_logic():
    """Analisa a lógica atual de corte das Meta Descriptions."""
    
    print("\n🔍 ANÁLISE DA LÓGICA DE CORTE ATUAL")
    print("=" * 50)
    
    # Simular diferentes cenários
    test_descriptions = [
        "Meta Description muito longa que excede o limite de 160 caracteres e por isso será cortada automaticamente pelo sistema para caber nos resultados de busca do Google e outros mecanismos de busca",
        "Meta Description de tamanho médio que está dentro do limite aceitável e não precisa ser cortada",
        "Meta Description curta que está bem abaixo do limite mínimo e pode ser expandida para melhor aproveitamento do espaço disponível"
    ]
    
    for i, desc in enumerate(test_descriptions, 1):
        print(f"\n📝 EXEMPLO {i}:")
        print(f"Original: '{desc}'")
        print(f"Comprimento: {len(desc)} caracteres")
        
        # Aplicar lógica atual
        if len(desc) > 160:
            # Lógica atual: cortar em 157 e adicionar "..."
            cut_desc = desc[:157] + "..."
            print(f"❌ CORTADA: '{cut_desc}'")
            print(f"Comprimento final: {len(cut_desc)} caracteres")
            print(f"Caracteres perdidos: {len(desc) - 157}")
        elif len(desc) < 140:
            print(f"⚠️  MUITO CURTA: Precisa ser expandida")
        else:
            print(f"✅ PERFEITA: Dentro dos limites (140-160 caracteres)")

def suggest_improvements():
    """Sugere melhorias para a lógica de Meta Description."""
    
    print("\n💡 SUGESTÕES DE MELHORIAS")
    print("=" * 50)
    
    print("1. 🎯 OTIMIZAR PROMPTS:")
    print("   - Instruir IA para gerar descrições entre 140-160 caracteres")
    print("   - Evitar frases muito longas ou repetitivas")
    print("   - Focar em benefícios principais do produto")
    
    print("\n2. 🔧 MELHORAR LÓGICA DE CORTE:")
    print("   - Cortar em frases completas, não no meio de palavras")
    print("   - Preservar informações mais importantes")
    print("   - Usar '...' apenas quando realmente necessário")
    
    print("\n3. 📏 AJUSTAR VALIDAÇÃO:")
    print("   - Verificar se o corte realmente melhora o resultado")
    print("   - Implementar fallback mais inteligente")
    print("   - Logs mais detalhados sobre quando e por que corta")

if __name__ == "__main__":
    test_meta_description_length()
    analyze_cutting_logic()
    suggest_improvements()
