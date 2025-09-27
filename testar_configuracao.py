#!/usr/bin/env python3
"""
Script para testar a configuração das API Keys e a interface Streamlit.
Verifica se as variáveis de ambiente estão configuradas corretamente.
"""

import os
from dotenv import load_dotenv

def test_env_configuration():
    """Testa a configuração das variáveis de ambiente."""
    
    print("🔍 Testando configuração das API Keys...")
    print("=" * 50)
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Verificar OpenAI API Key
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        print("✅ OpenAI API Key: Configurada")
        print(f"   Prefixo: {openai_key[:10]}...")
    else:
        print("❌ OpenAI API Key: Não configurada")
    
    # Verificar Gemini API Key
    gemini_key = os.getenv('GEMINI_API_KEY')
    if gemini_key:
        print("✅ Gemini API Key: Configurada")
        print(f"   Prefixo: {gemini_key[:10]}...")
    else:
        print("❌ Gemini API Key: Não configurada")
    
    print("=" * 50)
    
    # Verificar se pelo menos uma API Key está configurada
    if openai_key or gemini_key:
        print("✅ Pelo menos uma API Key está configurada")
        print("🚀 A interface Streamlit deve funcionar corretamente")
        
        # Mostrar provedores disponíveis
        available_providers = []
        if openai_key:
            available_providers.append("OpenAI")
        if gemini_key:
            available_providers.append("Gemini")
        
        print(f"📋 Provedores disponíveis: {', '.join(available_providers)}")
        
    else:
        print("❌ Nenhuma API Key configurada")
        print("💡 Configure pelo menos uma API Key no arquivo .env")
        print("📝 Use o arquivo env_example.txt como referência")
    
    print("=" * 50)
    
    # Instruções para executar
    print("🚀 Para executar a interface Streamlit:")
    print("   streamlit run app.py")
    
    print("\n📁 Arquivos importantes:")
    print("   - .env (suas API Keys)")
    print("   - env_example.txt (exemplo de configuração)")
    print("   - app.py (interface Streamlit)")
    print("   - product_description_enhancer.py (módulo principal)")

def main():
    """Função principal."""
    try:
        test_env_configuration()
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        print("💡 Verifique se o arquivo .env existe e está configurado corretamente")

if __name__ == "__main__":
    main()
