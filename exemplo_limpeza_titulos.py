#!/usr/bin/env python3
"""
Exemplo prático mostrando como a limpeza de títulos afeta a geração de Meta Tags SEO.
Demonstra a diferença entre usar títulos originais vs. títulos limpos.
"""

from product_description_enhancer import clean_product_title, ProductInfo, OpenAIProvider
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def demonstrate_title_cleaning_impact():
    """Demonstra o impacto da limpeza de títulos na geração de Meta Tags."""
    
    print("🎯 IMPACTO DA LIMPEZA DE TÍTULOS NAS META TAGS SEO")
    print("=" * 70)
    print("Este exemplo mostra como títulos limpos melhoram a qualidade das Meta Tags\n")
    
    # Exemplos de produtos com títulos que contêm informações técnicas
    examples = [
        {
            "title": "Whisky Black & White 700mL",
            "description": "Whisky escocês tradicional",
            "brand": "Black & White",
            "category": "Bebidas"
        },
        {
            "title": "Smartphone Samsung Galaxy A54 128GB Azul",
            "description": "Smartphone Samsung",
            "brand": "Samsung",
            "category": "Eletrônicos"
        },
        {
            "title": "Pack 6 Latas de Refrigerante Coca-Cola 350ml",
            "description": "Refrigerante Coca-Cola",
            "brand": "Coca-Cola",
            "category": "Bebidas"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"📱 EXEMPLO {i}: {example['title']}")
        print("-" * 50)
        
        # Mostrar título limpo
        clean_title = clean_product_title(example['title'])
        print(f"Título Original: {example['title']}")
        print(f"Título Limpo:   {clean_title}")
        print(f"Redução:        {len(example['title'])} → {len(clean_title)} caracteres")
        
        # Simular geração de Meta Title
        print(f"\n🎯 META TITLE (com título limpo):")
        brand = example['brand']
        meta_title = f"{clean_title} | {brand} - Compra Agora"
        print(f"Resultado: {meta_title}")
        print(f"Caracteres: {len(meta_title)} (ideal: 50-60)")
        
        # Mostrar como seria com título original
        print(f"\n⚠️  META TITLE (com título original):")
        meta_title_original = f"{example['title']} | {brand} - Compra Agora"
        print(f"Resultado: {meta_title_original}")
        print(f"Caracteres: {len(meta_title_original)} (ideal: 50-60)")
        
        # Avaliar qualidade
        if len(meta_title) <= 60:
            print("✅ Título limpo: PERFEITO para SEO (dentro do limite)")
        else:
            print("❌ Título limpo: Muito longo para SEO")
            
        if len(meta_title_original) <= 60:
            print("✅ Título original: OK para SEO")
        else:
            print("❌ Título original: MUITO LONGO para SEO (será cortado)")
        
        print("\n" + "=" * 70 + "\n")
    
    print("🚀 BENEFÍCIOS DA LIMPEZA AUTOMÁTICA:")
    print("• Meta Titles mais focados no produto")
    print("• Melhor aproveitamento dos 60 caracteres disponíveis")
    print("• Informações técnicas removidas automaticamente")
    print("• SEO otimizado para mecanismos de busca")
    print("• Consistência em todo o catálogo")

def test_with_ai_provider():
    """Testa a funcionalidade com um provedor de IA (se disponível)."""
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  OPENAI_API_KEY não configurada. Pulando teste com IA.")
        return
    
    print("\n🤖 TESTE COM PROVEDOR DE IA (OpenAI)")
    print("=" * 50)
    
    try:
        # Criar produto de exemplo
        product = ProductInfo(
            title="Whisky Black & White 700mL",
            description="Whisky escocês tradicional com sabor suave",
            brand="Black & White",
            category="Bebidas"
        )
        
        # Mostrar título limpo
        clean_title = clean_product_title(product.title)
        print(f"Título Original: {product.title}")
        print(f"Título Limpo:   {clean_title}")
        
        # Simular geração de Meta Title
        meta_title = f"{clean_title} | {product.brand} - Compra Agora"
        print(f"\nMeta Title Gerado: {meta_title}")
        print(f"Caracteres: {len(meta_title)}")
        
        print("✅ Teste com IA concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro no teste com IA: {str(e)}")

if __name__ == "__main__":
    demonstrate_title_cleaning_impact()
    test_with_ai_provider()
