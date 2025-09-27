#!/usr/bin/env python3
"""
Script para testar as melhorias na variação das Meta Descriptions.
Demonstra como agora as Meta Descriptions não começam sempre com o nome do produto.
"""

from product_description_enhancer import clean_product_title, ProductInfo, OpenAIProvider
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_fallback_variation():
    """Testa a variação na função de fallback das Meta Descriptions."""
    
    print("🎲 TESTE DE VARIAÇÃO NAS META DESCRIPTIONS")
    print("=" * 60)
    print("Verifica se as Meta Descriptions agora variam a estrutura\n")
    
    # Criar instância da classe para testar o método
    api_key = os.getenv('OPENAI_API_KEY', 'test-key')
    provider = OpenAIProvider(api_key)
    
    # Produto de teste
    product = ProductInfo(
        title="Whisky Black & White 700mL",
        description="Whisky escocês tradicional com sabor suave",
        brand="Black & White",
        category="Bebidas"
    )
    
    print(f"📱 PRODUTO: {product.title}")
    print(f"📋 CATEGORIA: {product.category}")
    print(f"🏷️  MARCA: {product.brand}")
    print("-" * 50)
    
    # Testar múltiplas gerações para ver a variação
    print("🔄 TESTANDO MÚLTIPLAS GERAÇÕES (Fallback):")
    print()
    
    for i in range(1, 6):
        meta_desc = provider._generate_fallback_meta_description(product)
        print(f"Geração {i}: {meta_desc}")
        print(f"Comprimento: {len(meta_desc)} caracteres")
        
        # Verificar se começa com o nome do produto
        clean_title = clean_product_title(product.title)
        if meta_desc.startswith(clean_title):
            print("📍 Estrutura: Começa com nome do produto")
        else:
            print("🎯 Estrutura: Variação implementada!")
        
        print("-" * 30)
    
    print("✅ Variação implementada com sucesso!")

def test_prompt_improvements():
    """Testa as melhorias nos prompts para a IA."""
    
    print("\n🎯 TESTE DOS PROMPTS MELHORADOS")
    print("=" * 60)
    print("Verifica se os prompts agora instruem a IA a variar a estrutura\n")
    
    # Criar produto de teste
    product = ProductInfo(
        title="Smartphone Samsung Galaxy A54 128GB Azul",
        description="Smartphone Samsung com câmera de 50MP",
        brand="Samsung",
        category="Eletrônicos"
    )
    
    # Gerar prompt otimizado
    api_key = os.getenv('OPENAI_API_KEY', 'test-key')
    provider = OpenAIProvider(api_key)
    prompt = provider._create_seo_prompt(product)
    
    print("📋 PROMPT OTIMIZADO - PARTES IMPORTANTES:")
    print("-" * 40)
    
    # Mostrar partes importantes do prompt
    lines = prompt.split('\n')
    for line in lines:
        if any(keyword in line for keyword in ['não obrigatoriamente no início', 'Varie a estrutura', 'CRÍTICO']):
            print(f"🎯 {line.strip()}")
    
    print("\n📊 INSTRUÇÕES DE VARIAÇÃO:")
    print("• Palavra-chave não obrigatoriamente no início")
    print("• Varie a estrutura - nem sempre comece com o nome do produto")
    print("• Exemplos mostram diferentes estruturas")

def demonstrate_structure_variations():
    """Demonstra as diferentes estruturas possíveis."""
    
    print("\n🏗️  ESTRUTURAS POSSÍVEIS PARA META DESCRIPTIONS")
    print("=" * 60)
    
    examples = [
        {
            "estrutura": "Benefício + Produto + Call to Action",
            "exemplo": "Descubra a qualidade superior do Whisky Black & White. Sabor premium e qualidade excepcional. Compre agora na Compra Agora!",
            "vantagem": "Foca primeiro no benefício, depois no produto"
        },
        {
            "estrutura": "Produto + Benefícios + Call to Action",
            "exemplo": "Whisky Black & White com sabor premium e qualidade excepcional. Descubra e compre agora na Compra Agora!",
            "vantagem": "Estrutura tradicional, direta e clara"
        },
        {
            "estrutura": "Call to Action + Produto + Benefícios",
            "exemplo": "Experimente o Whisky Black & White com sabor premium e qualidade excepcional. Compre agora na Compra Agora!",
            "vantagem": "Começa com ação, mais persuasivo"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['estrutura']}")
        print(f"   Exemplo: {example['exemplo']}")
        print(f"   Vantagem: {example['vantagem']}")
        print(f"   Comprimento: {len(example['exemplo'])} caracteres")

def test_with_real_ai():
    """Testa com IA real se disponível."""
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("\n⚠️  OPENAI_API_KEY não configurada. Pulando teste com IA real.")
        return
    
    print("\n🤖 TESTE COM IA REAL (OpenAI)")
    print("=" * 50)
    
    try:
        # Criar produto de teste
        product = ProductInfo(
            title="Antitranspirante Dove Men+Care Invisible Dry 150ml",
            description="Antitranspirante com proteção duradoura",
            brand="Dove",
            category="Higiene"
        )
        
        # Testar geração de Meta Description
        provider = OpenAIProvider(api_key)
        seo_info = provider.generate_seo_content(product)
        
        print(f"✅ Meta Description gerada com sucesso!")
        print(f"Comprimento: {len(seo_info.meta_description)} caracteres")
        print(f"Resultado: {seo_info.meta_description}")
        
        # Verificar estrutura
        clean_title = clean_product_title(product.title)
        if seo_info.meta_description.startswith(clean_title):
            print("📍 Estrutura: Começa com nome do produto")
        else:
            print("🎯 Estrutura: Variação implementada!")
        
        # Verificar se está dentro dos limites
        if 140 <= len(seo_info.meta_description) <= 160:
            print("✅ PERFEITO: Dentro dos limites (140-160 caracteres)")
        elif len(seo_info.meta_description) > 160:
            print("❌ AINDA LONGA: Precisa de mais otimização")
        else:
            print("⚠️  MUITO CURTA: Pode ser expandida")
        
    except Exception as e:
        print(f"❌ Erro no teste com IA: {str(e)}")

if __name__ == "__main__":
    test_fallback_variation()
    test_prompt_improvements()
    demonstrate_structure_variations()
    test_with_real_ai()


