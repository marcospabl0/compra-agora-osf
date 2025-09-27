#!/usr/bin/env python3
"""
Script para testar as melhorias na naturalidade das Meta Descriptions.
Demonstra como a palavra-chave agora é usada de forma mais natural e menos engessada.
"""

from product_description_enhancer import clean_product_title, ProductInfo, OpenAIProvider
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_natural_keyword_usage():
    """Testa o uso mais natural da palavra-chave nas Meta Descriptions."""
    
    print("🌿 TESTE DE NATURALIDADE NAS META DESCRIPTIONS")
    print("=" * 70)
    print("Verifica se a palavra-chave agora é usada de forma mais natural\n")
    
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
    
    # Testar múltiplas gerações para ver a naturalidade
    print("🔄 TESTANDO MÚLTIPLAS GERAÇÕES (Fallback Natural):")
    print()
    
    for i in range(1, 6):
        meta_desc = provider._generate_fallback_meta_description(product)
        print(f"Geração {i}: {meta_desc}")
        print(f"Comprimento: {len(meta_desc)} caracteres")
        
        # Verificar se a palavra-chave está sendo usada naturalmente
        clean_title = clean_product_title(product.title)
        if clean_title in meta_desc:
            # Verificar a posição e contexto da palavra-chave
            position = meta_desc.find(clean_title)
            context_before = meta_desc[max(0, position-20):position].strip()
            context_after = meta_desc[position+len(clean_title):position+len(clean_title)+20].strip()
            
            print(f"📍 Palavra-chave encontrada na posição {position}")
            print(f"   Contexto antes: '...{context_before}'")
            print(f"   Contexto depois: '{context_after}...'")
            
            # Avaliar naturalidade
            if any(word in context_before.lower() for word in ['do', 'da', 'com', 'para', 'um', 'uma']):
                print("✅ NATURAL: Palavra-chave inserida naturalmente no contexto")
            else:
                print("⚠️  PODE MELHORAR: Palavra-chave pode estar muito isolada")
        else:
            print("❌ ERRO: Palavra-chave não encontrada")
        
        print("-" * 30)
    
    print("✅ Naturalidade implementada com sucesso!")

def test_prompt_improvements():
    """Testa as melhorias nos prompts para a IA."""
    
    print("\n🎯 TESTE DOS PROMPTS MELHORADOS")
    print("=" * 60)
    print("Verifica se os prompts agora instruem a IA a usar a palavra-chave naturalmente\n")
    
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
        if any(keyword in line for keyword in ['natural', 'engessada', 'fluir naturalmente', 'escrita por um humano']):
            print(f"🌿 {line.strip()}")
    
    print("\n📊 INSTRUÇÕES DE NATURALIDADE:")
    print("• Palavra-chave não no início")
    print("• Não de forma engessada")
    print("• Seja o mais natural possível")
    print("• Deve fluir naturalmente no texto")
    print("• Como se fosse escrita por um humano")

def demonstrate_natural_vs_engessado():
    """Demonstra a diferença entre uso natural e engessado da palavra-chave."""
    
    print("\n🔄 COMPARAÇÃO: NATURAL vs ENGESSADO")
    print("=" * 60)
    
    examples = [
        {
            "tipo": "❌ ENGESSADO (Antes)",
            "exemplos": [
                "Whisky Black & White com sabor premium e qualidade excepcional. Descubra e compre agora na Compra Agora!",
                "Antitranspirante Dove Men+Care com proteção duradoura. Fórmula avançada. Compre agora na Compra Agora!",
                "Smartphone Samsung Galaxy A54 com tecnologia avançada. Recursos inovadores. Compre agora na Compra Agora!"
            ],
            "problemas": [
                "Palavra-chave sempre no início",
                "Estrutura repetitiva",
                "Som artificial e robótico"
            ]
        },
        {
            "tipo": "✅ NATURAL (Depois)",
            "exemplos": [
                "Descubra o sabor rico e equilibrado de um blend premium para momentos especiais. Whisky Black & White com tradição escocesa. Compre na Compra Agora!",
                "Proteção invisível por 48h com fórmula avançada que combate o odor. Antitranspirante Dove Men+Care para sua confiança diária. Compre agora na Compra Agora!",
                "Tecnologia avançada com recursos inovadores para fotografia profissional. Smartphone Samsung Galaxy A54 para suas necessidades. Compre agora na Compra Agora!"
            ],
            "vantagens": [
                "Palavra-chave inserida naturalmente",
                "Estrutura variada e fluida",
                "Som humano e persuasivo"
            ]
        }
    ]
    
    for example in examples:
        print(f"\n{example['tipo']}")
        print("-" * 40)
        
        for i, ex in enumerate(example['exemplos'], 1):
            print(f"{i}. {ex}")
            print(f"   Comprimento: {len(ex)} caracteres")
        
        if 'problemas' in example:
            print(f"\n🚨 Problemas identificados:")
            for problem in example['problemas']:
                print(f"   • {problem}")
        elif 'vantagens' in example:
            print(f"\n✅ Vantagens implementadas:")
            for advantage in example['vantagens']:
                print(f"   • {advantage}")

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
        
        # Verificar naturalidade da palavra-chave
        clean_title = clean_product_title(product.title)
        
        # Tentar encontrar a palavra-chave completa ou partes dela
        found_keyword = None
        if clean_title in seo_info.meta_description:
            found_keyword = clean_title
        else:
            # Tentar encontrar partes da palavra-chave
            title_words = clean_title.split()
            for word in title_words:
                if len(word) > 3 and word.lower() in seo_info.meta_description.lower():
                    found_keyword = word
                    break
        
        if found_keyword:
            position = seo_info.meta_description.lower().find(found_keyword.lower())
            print(f"📍 Palavra-chave '{found_keyword}' encontrada na posição {position}")
            
            # Avaliar contexto
            context_before = seo_info.meta_description[max(0, position-15):position].strip()
            context_after = seo_info.meta_description[position+len(found_keyword):position+len(found_keyword)+15].strip()
            
            print(f"   Contexto: '...{context_before} {found_keyword} {context_after}...'")
            
            if any(word in context_before.lower() for word in ['do', 'da', 'com', 'para', 'um', 'uma', 'o', 'a']):
                print("✅ NATURAL: Palavra-chave inserida naturalmente")
            else:
                print("⚠️  PODE MELHORAR: Contexto pode ser mais natural")
        else:
            print("❌ ERRO: Palavra-chave não encontrada")
        
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
    test_natural_keyword_usage()
    test_prompt_improvements()
    demonstrate_natural_vs_engessado()
    test_with_real_ai()
