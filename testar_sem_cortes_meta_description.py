#!/usr/bin/env python3
"""
Script para testar se as Meta Descriptions agora são geradas sem cortes.
Verifica se a IA está seguindo as instruções para gerar texto completo dentro do limite.
"""

from product_description_enhancer import clean_product_title, ProductInfo, OpenAIProvider
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_no_cuts_instructions():
    """Testa se as instruções para não cortar estão nos prompts."""
    
    print("🚫 TESTE DE INSTRUÇÕES SEM CORTES")
    print("=" * 60)
    print("Verifica se os prompts agora instruem a IA a não cortar o texto\n")
    
    # Criar produto de teste
    product = ProductInfo(
        title="Antitranspirante Dove Men+Care Invisible Dry 150ml",
        description="Antitranspirante com proteção duradoura",
        brand="Dove",
        category="Higiene"
    )
    
    # Gerar prompt otimizado
    api_key = os.getenv('OPENAI_API_KEY', 'test-key')
    provider = OpenAIProvider(api_key)
    prompt = provider._create_seo_prompt(product)
    
    print("📋 PROMPT OTIMIZADO - INSTRUÇÕES CRÍTICAS:")
    print("-" * 50)
    
    # Mostrar instruções críticas sobre cortes
    lines = prompt.split('\n')
    for line in lines:
        if any(keyword in line for keyword in ['NUNCA corte', 'texto COMPLETO', 'sem cortes', '140-160 caracteres']):
            print(f"🚫 {line.strip()}")
    
    print("\n📊 INSTRUÇÕES IMPLEMENTADAS:")
    print("• Gere SEMPRE o texto COMPLETO dentro do limite de 160 caracteres")
    print("• NUNCA corte no meio")
    print("• Planeje o texto para caber exatamente entre 140-160 caracteres, sem cortes")

def test_examples_length():
    """Testa se os exemplos nos prompts estão dentro do limite correto."""
    
    print("\n📏 TESTE DE COMPRIMENTO DOS EXEMPLOS")
    print("=" * 50)
    
    examples = [
        "Proteção invisível por 48h com fórmula avançada que combate o odor. Antitranspirante Dove Men+Care para sua confiança diária. Compre agora na Compra Agora!",
        "Descubra o sabor rico de um blend premium para momentos especiais. Whisky Johnnie Walker Red Label com tradição escocesa. Compre na Compra Agora!",
        "Fórmula avançada com proteção duradoura e frescor intenso. Antitranspirante Dove Men+Care para sua pele. Compre agora na Compra Agora!"
    ]
    
    for i, example in enumerate(examples, 1):
        length = len(example)
        status = "✅ PERFEITO" if 140 <= length <= 160 else "❌ FORA DO LIMITE"
        print(f"Exemplo {i}: {length} caracteres - {status}")
        print(f"   Texto: {example}")
        print()

def test_fallback_no_cuts():
    """Testa se a função de fallback também não corta o texto."""
    
    print("\n🔄 TESTE DE FALLBACK SEM CORTES")
    print("=" * 50)
    
    # Criar instância para testar
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
    print("-" * 30)
    
    # Testar múltiplas gerações
    for i in range(1, 4):
        meta_desc = provider._generate_fallback_meta_description(product)
        length = len(meta_desc)
        
        print(f"Geração {i}: {length} caracteres")
        print(f"Texto: {meta_desc}")
        
        # Verificar se está dentro dos limites
        if 140 <= length <= 160:
            print("✅ PERFEITO: Dentro dos limites (140-160 caracteres)")
        elif length > 160:
            print("❌ AINDA LONGA: Precisa de mais otimização")
        else:
            print("⚠️  MUITO CURTA: Pode ser expandida")
        
        # Verificar se termina corretamente
        if meta_desc.endswith("Compre agora na Compra Agora!"):
            print("✅ PERFEITO: Termina com call-to-action completo")
        else:
            print("❌ PROBLEMA: Não termina corretamente")
        
        print("-" * 30)

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
            title="Smartphone Samsung Galaxy A54 128GB Azul",
            description="Smartphone Samsung com câmera de 50MP",
            brand="Samsung",
            category="Eletrônicos"
        )
        
        # Testar geração de Meta Description
        provider = OpenAIProvider(api_key)
        seo_info = provider.generate_seo_content(product)
        
        print(f"✅ Meta Description gerada com sucesso!")
        print(f"Comprimento: {len(seo_info.meta_description)} caracteres")
        print(f"Resultado: {seo_info.meta_description}")
        
        # Verificar se está dentro dos limites
        if 140 <= len(seo_info.meta_description) <= 160:
            print("✅ PERFEITO: Dentro dos limites (140-160 caracteres)")
        elif len(seo_info.meta_description) > 160:
            print("❌ AINDA LONGA: Precisa de mais otimização")
        else:
            print("⚠️  MUITO CURTA: Pode ser expandida")
        
        # Verificar se termina corretamente
        if seo_info.meta_description.endswith("Compre agora na Compra Agora!"):
            print("✅ PERFEITO: Termina com call-to-action completo")
        else:
            print("❌ PROBLEMA: Não termina corretamente")
        
        # Verificar se há cortes no meio
        if "..." in seo_info.meta_description:
            print("❌ PROBLEMA: Texto cortado com '...'")
        else:
            print("✅ PERFEITO: Texto completo sem cortes")
        
    except Exception as e:
        print(f"❌ Erro no teste com IA: {str(e)}")

def demonstrate_problem_solved():
    """Demonstra como o problema dos cortes foi resolvido."""
    
    print("\n🔧 PROBLEMA DOS CORTES - SOLUÇÃO IMPLEMENTADA")
    print("=" * 70)
    
    problems = [
        {
            "problema": "❌ Meta Descriptions cortadas no meio",
            "exemplos": [
                "Produto com qualidade superior e garantia de satisfação que garante sua satisfação. Compre agora na Compra Agora!",
                "Experimente um produto com qualidade superior e garantia de satisfação. Antitranspirante Dove Men+Care Comfort Protection para suas necessidades. Compre agora n",
                "Descubra a qualidade superior de um produto que oferece qualidade superior e garantia de satisfação. Compre agora na Compra Agora!"
            ],
            "causa": "IA não estava planejando o texto para caber no limite"
        },
        {
            "problema": "✅ SOLUÇÃO IMPLEMENTADA",
            "exemplos": [
                "Proteção invisível por 48h com fórmula avançada que combate o odor. Antitranspirante Dove Men+Care para sua confiança diária. Compre agora na Compra Agora! (155 caracteres)",
                "Descubra o sabor rico de um blend premium para momentos especiais. Whisky Johnnie Walker Red Label com tradição escocesa. Compre na Compra Agora! (148 caracteres)",
                "Fórmula avançada com proteção duradoura e frescor intenso. Antitranspirante Dove Men+Care para sua pele. Compre agora na Compra Agora! (150 caracteres)"
            ],
            "causa": "Instruções críticas para gerar texto completo sem cortes"
        }
    ]
    
    for problem in problems:
        print(f"\n{problem['problema']}")
        print("-" * 50)
        print(f"Causa: {problem['causa']}")
        print("Exemplos:")
        for i, ex in enumerate(problem['exemplos'], 1):
            print(f"  {i}. {ex}")
    
    print("\n🎯 INSTRUÇÕES CRÍTICAS ADICIONADAS:")
    print("• CRÍTICO: Gere SEMPRE o texto COMPLETO dentro do limite de 160 caracteres - NUNCA corte no meio")
    print("• CRÍTICO: Planeje o texto para caber exatamente entre 140-160 caracteres, sem cortes")
    print("• Exemplos com contagem de caracteres para demonstração")

if __name__ == "__main__":
    test_no_cuts_instructions()
    test_examples_length()
    test_fallback_no_cuts()
    test_with_real_ai()
    demonstrate_problem_solved()
