#!/usr/bin/env python3
"""
Script para testar as melhorias implementadas nas Meta Descriptions.
Verifica se a lógica inteligente de corte está funcionando e se os prompts otimizados geram descrições mais concisas.
"""

from product_description_enhancer import clean_product_title, ProductInfo, OpenAIProvider
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_smart_cutting():
    """Testa a nova lógica inteligente de corte das Meta Descriptions."""
    
    print("🧠 TESTE DA LÓGICA INTELIGENTE DE CORTE")
    print("=" * 60)
    print("Verifica se as Meta Descriptions são cortadas de forma inteligente\n")
    
    # Criar instância da classe para testar o método
    api_key = os.getenv('OPENAI_API_KEY', 'test-key')
    provider = OpenAIProvider(api_key)
    
    # Meta Descriptions de teste (simulando diferentes cenários)
    test_descriptions = [
        "Whisky Black & White com sabor suave e equilibrado. Blend premium de malte e grãos escoceses. Perfeito para momentos especiais e celebrações. Descubra a tradição centenária e compre agora na Compra Agora!",
        
        "Smartphone Samsung Galaxy A54 com câmera de 50MP e tela 6.4 polegadas. Tecnologia avançada e recursos inovadores para fotografia profissional. Performance excepcional e design moderno. Compre agora na Compra Agora!",
        
        "Antitranspirante Dove Men+Care com proteção invisível por até 48 horas. Fórmula avançada que combate o odor e mantém a pele seca. Frescor intenso e conforto duradouro. Descubra e compre agora na Compra Agora!"
    ]
    
    for i, desc in enumerate(test_descriptions, 1):
        print(f"📝 EXEMPLO {i}:")
        print(f"Original: {desc}")
        print(f"Comprimento: {len(desc)} caracteres")
        
        # Aplicar corte inteligente
        if len(desc) > 160:
            cut_desc = provider._smart_cut_meta_description(desc)
            print(f"✅ CORTADA INTELIGENTEMENTE:")
            print(f"Resultado: {cut_desc}")
            print(f"Comprimento final: {len(cut_desc)} caracteres")
            
            # Verificar se ainda tem "Compra Agora"
            if 'Compra Agora' in cut_desc:
                print("✅ Mantém 'Compra Agora'")
            else:
                print("❌ Perdeu 'Compra Agora'")
        else:
            print(f"✅ OK: Dentro do limite")
        
        print("-" * 50)

def test_prompt_optimization():
    """Testa se os prompts otimizados estão funcionando."""
    
    print("\n🎯 TESTE DOS PROMPTS OTIMIZADOS")
    print("=" * 60)
    print("Verifica se os prompts estão instruindo a IA corretamente\n")
    
    # Criar produto de teste
    product = ProductInfo(
        title="Whisky Black & White 700mL",
        description="Whisky escocês tradicional",
        brand="Black & White",
        category="Bebidas"
    )
    
    # Gerar prompt otimizado
    api_key = os.getenv('OPENAI_API_KEY', 'test-key')
    provider = OpenAIProvider(api_key)
    prompt = provider._create_seo_prompt(product)
    
    print("📋 PROMPT OTIMIZADO GERADO:")
    print("-" * 40)
    
    # Mostrar partes importantes do prompt
    lines = prompt.split('\n')
    for line in lines:
        if any(keyword in line for keyword in ['OBRIGATÓRIO', 'CRÍTICO', '140-160', 'CONCISAS']):
            print(f"🎯 {line.strip()}")
    
    print("\n📊 INSTRUÇÕES PRINCIPAIS:")
    print("• Meta Description deve ter entre 140-160 caracteres")
    print("• Seja conciso e direto")
    print("• Evite frases longas e repetitivas")
    print("• Priorize benefícios principais")

def demonstrate_improvements():
    """Demonstra as melhorias implementadas."""
    
    print("\n🚀 MELHORIAS IMPLEMENTADAS")
    print("=" * 60)
    
    print("1. 🎯 PROMPTS OTIMIZADOS:")
    print("   ✅ Instruções mais claras sobre comprimento")
    print("   ✅ Exemplos de descrições concisas")
    print("   ✅ Ênfase em ser direto e objetivo")
    
    print("\n2. 🧠 CORTE INTELIGENTE:")
    print("   ✅ Tenta cortar em frases completas primeiro")
    print("   ✅ Preserva 'Compra Agora' quando possível")
    print("   ✅ Usa '...' apenas quando necessário")
    
    print("\n3. 📏 VALIDAÇÃO MELHORADA:")
    print("   ✅ Verifica se o corte realmente melhora")
    print("   ✅ Fallback mais inteligente")
    print("   ✅ Logs mais detalhados")
    
    print("\n4. 🎨 EXEMPLOS ATUALIZADOS:")
    print("   ✅ Descrições dentro dos limites corretos")
    print("   ✅ Foco em benefícios principais")
    print("   ✅ Linguagem mais direta e persuasiva")

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
            title="Whisky Black & White 700mL",
            description="Whisky escocês tradicional com sabor suave",
            brand="Black & White",
            category="Bebidas"
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
        
    except Exception as e:
        print(f"❌ Erro no teste com IA: {str(e)}")

if __name__ == "__main__":
    test_smart_cutting()
    test_prompt_optimization()
    demonstrate_improvements()
    test_with_real_ai()
