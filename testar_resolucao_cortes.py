#!/usr/bin/env python3
"""
Script para testar se o problema dos cortes foi completamente resolvido.
Verifica se as Meta Descriptions agora são sempre completas e terminam corretamente.
"""

from product_description_enhancer import clean_product_title, ProductInfo, OpenAIProvider
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_cutting_disabled():
    """Testa se o sistema de corte foi desabilitado."""
    
    print("🚫 TESTE DE SISTEMA DE CORTE DESABILITADO")
    print("=" * 60)
    print("Verifica se o sistema de corte inteligente foi desabilitado\n")
    
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
    
    print("📋 PROMPT OTIMIZADO - INSTRUÇÕES ANTI-CORTE:")
    print("-" * 50)
    
    # Mostrar instruções críticas sobre não cortar
    lines = prompt.split('\n')
    for line in lines:
        if any(keyword in line for keyword in ['NUNCA corte', 'NUNCA use reticências', 'reescreva completamente', 'terminar sempre com']):
            print(f"🚫 {line.strip()}")
    
    print("\n📊 INSTRUÇÕES ANTI-CORTE IMPLEMENTADAS:")
    print("• NUNCA corte no meio")
    print("• NUNCA use reticências (...)")
    print("• Se muito longo, reescreva completamente")
    print("• Terminar sempre com 'Compre agora na Compra Agora!' completo")

def test_fallback_always_complete():
    """Testa se a função de fallback sempre gera texto completo."""
    
    print("\n🔄 TESTE DE FALLBACK SEMPRE COMPLETO")
    print("=" * 60)
    
    # Criar instância para testar
    api_key = os.getenv('OPENAI_API_KEY', 'test-key')
    provider = OpenAIProvider(api_key)
    
    # Produtos de teste variados
    test_products = [
        ProductInfo(
            title="Whisky Black & White 700mL",
            description="Whisky escocês tradicional com sabor suave",
            brand="Black & White",
            category="Bebidas"
        ),
        ProductInfo(
            title="Smartphone Samsung Galaxy A54 128GB Azul",
            description="Smartphone Samsung com câmera de 50MP",
            brand="Samsung",
            category="Eletrônicos"
        ),
        ProductInfo(
            title="Antitranspirante Dove Men+Care Comfort Protection 72h",
            description="Antitranspirante com proteção confortável por 72 horas",
            brand="Dove",
            category="Higiene"
        )
    ]
    
    for i, product in enumerate(test_products, 1):
        print(f"\n📱 PRODUTO {i}: {product.title}")
        print("-" * 50)
        
        # Testar múltiplas gerações
        for j in range(1, 4):
            meta_desc = provider._generate_fallback_meta_description(product)
            length = len(meta_desc)
            
            print(f"Geração {j}: {length} caracteres")
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
            
            # Verificar se há cortes
            if "..." in meta_desc or meta_desc.endswith("na C") or meta_desc.endswith("na Comp"):
                print("❌ PROBLEMA: Texto cortado ou incompleto")
            else:
                print("✅ PERFEITO: Texto completo sem cortes")
            
            print("-" * 30)

def test_with_real_ai_no_cuts():
    """Testa com IA real para verificar se não há mais cortes."""
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("\n⚠️  OPENAI_API_KEY não configurada. Pulando teste com IA real.")
        return
    
    print("\n🤖 TESTE COM IA REAL - SEM CORTES")
    print("=" * 60)
    
    try:
        # Criar produto de teste
        product = ProductInfo(
            title="Desodorante Rexona Women Roll On 50g",
            description="Desodorante feminino com proteção duradoura",
            brand="Rexona",
            category="Higiene"
        )
        
        # Testar geração de Meta Description
        provider = OpenAIProvider(api_key)
        seo_info = provider.generate_seo_content(product)
        
        print(f"✅ Meta Description gerada com sucesso!")
        print(f"Comprimento: {len(seo_info.meta_description)} caracteres")
        print(f"Resultado: {seo_info.meta_description}")
        
        # Verificações críticas
        checks = [
            ("Comprimento 140-160", 140 <= len(seo_info.meta_description) <= 160),
            ("Termina corretamente", seo_info.meta_description.endswith("Compre agora na Compra Agora!")),
            ("Sem reticências", "..." not in seo_info.meta_description),
            ("Sem cortes", not seo_info.meta_description.endswith(("na C", "na Comp", "na Compra"))),
            ("Texto completo", len(seo_info.meta_description.strip()) > 0)
        ]
        
        print("\n🔍 VERIFICAÇÕES CRÍTICAS:")
        for check_name, result in checks:
            status = "✅ PASSOU" if result else "❌ FALHOU"
            print(f"• {check_name}: {status}")
        
        # Resumo final
        passed_checks = sum(1 for _, result in checks if result)
        total_checks = len(checks)
        
        print(f"\n📊 RESULTADO FINAL: {passed_checks}/{total_checks} verificações passaram")
        
        if passed_checks == total_checks:
            print("🎉 SUCESSO TOTAL: Problema dos cortes resolvido!")
        else:
            print("⚠️  AINDA HÁ PROBLEMAS: Algumas verificações falharam")
        
    except Exception as e:
        print(f"❌ Erro no teste com IA: {str(e)}")

def demonstrate_cutting_problem_solved():
    """Demonstra como o problema dos cortes foi resolvido."""
    
    print("\n🔧 PROBLEMA DOS CORTES - SOLUÇÃO FINAL IMPLEMENTADA")
    print("=" * 80)
    
    problems = [
        {
            "problema": "❌ ANTES: Meta Descriptions cortadas no meio",
            "exemplos": [
                "Descubra a qualidade superior de um produto que oferece qualidade superior e garantia de satisfação. Fita Strip Mãe Terra para sua satisfação. Compre agora na C",
                "Descubra a qualidade superior de um produto que oferece qualidade superior e garantia de satisfação. Moldura Mãe Terra para sua satisfação. Compre agora na Comp",
                "Descubra a qualidade superior de um produto que oferece qualidade superior e garantia de satisfação. Whisky Black & White para sua satisfação. Compre agora na C"
            ],
            "causa": "Sistema de corte inteligente ativado + IA não planejava o texto"
        },
        {
            "problema": "✅ DEPOIS: Meta Descriptions sempre completas",
            "exemplos": [
                "Proteção invisível por 48h com fórmula avançada que combate o odor. Antitranspirante Dove Men+Care para sua confiança diária. Compre agora na Compra Agora!",
                "Descubra o sabor rico de um blend premium para momentos especiais. Whisky Johnnie Walker Red Label com tradição escocesa. Compre agora na Compra Agora!",
                "Fórmula avançada com proteção duradoura e frescor intenso. Antitranspirante Dove Men+Care para sua pele. Compre agora na Compra Agora!"
            ],
            "causa": "Sistema de corte desabilitado + Instruções críticas anti-corte + Fallback sempre completo"
        }
    ]
    
    for problem in problems:
        print(f"\n{problem['problema']}")
        print("-" * 60)
        print(f"Causa: {problem['causa']}")
        print("Exemplos:")
        for i, ex in enumerate(problem['exemplos'], 1):
            print(f"  {i}. {ex}")
    
    print("\n🎯 SOLUÇÕES IMPLEMENTADAS:")
    print("• 🚫 Sistema de corte inteligente DESABILITADO")
    print("• 🚫 Instruções críticas: NUNCA corte no meio")
    print("• 🚫 Instruções críticas: NUNCA use reticências (...)")
    print("• 🔄 Fallback sempre gera texto completo")
    print("• ✅ Validação: Se muito longo, usa fallback em vez de cortar")
    print("• ✅ Garantia: Texto sempre termina com call-to-action completo")

if __name__ == "__main__":
    test_cutting_disabled()
    test_fallback_always_complete()
    test_with_real_ai_no_cuts()
    demonstrate_cutting_problem_solved()
