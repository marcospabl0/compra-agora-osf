#!/usr/bin/env python3
"""
Script para verificar se o projeto está pronto para deploy no Streamlit Cloud.
"""

import os
import sys
from pathlib import Path

def verificar_arquivos_necessarios():
    """Verifica se todos os arquivos necessários estão presentes."""
    arquivos_necessarios = [
        'app.py',
        'product_description_enhancer.py',
        'config.json',
        'requirements-streamlit-cloud.txt',
        '.streamlit/config.toml',
        'exemplo_catalogo_streamlit.xlsx'
    ]
    
    arquivos_faltando = []
    for arquivo in arquivos_necessarios:
        if not Path(arquivo).exists():
            arquivos_faltando.append(arquivo)
    
    return arquivos_faltando

def verificar_imports():
    """Verifica se os imports principais funcionam."""
    try:
        import streamlit as st
        import pandas as pd
        import openai
        import google.generativeai as genai
        from dotenv import load_dotenv
        print("✅ Todos os imports principais funcionam")
        return True
    except ImportError as e:
        print(f"❌ Erro de import: {e}")
        return False

def verificar_configuracao():
    """Verifica se a configuração está correta."""
    try:
        import json
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Verificar se as configurações essenciais estão presentes
        required_keys = ['seo_settings', 'prompt_settings', 'prohibited_phrases']
        for key in required_keys:
            if key not in config:
                print(f"❌ Chave '{key}' não encontrada em config.json")
                return False
        
        print("✅ Configuração JSON está correta")
        return True
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False

def verificar_requirements():
    """Verifica se o arquivo requirements está correto."""
    try:
        with open('requirements-streamlit-cloud.txt', 'r') as f:
            requirements = f.read()
        
        # Verificar se as dependências essenciais estão presentes
        essential_deps = [
            'streamlit',
            'pandas',
            'openai',
            'google-generativeai',
            'python-dotenv'
        ]
        
        for dep in essential_deps:
            if dep not in requirements:
                print(f"❌ Dependência '{dep}' não encontrada em requirements")
                return False
        
        print("✅ Arquivo requirements está correto")
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar requirements: {e}")
        return False

def verificar_streamlit_config():
    """Verifica se a configuração do Streamlit está correta."""
    try:
        config_path = Path('.streamlit/config.toml')
        if not config_path.exists():
            print("❌ Arquivo .streamlit/config.toml não encontrado")
            return False
        
        with open(config_path, 'r') as f:
            config_content = f.read()
        
        # Verificar se as configurações essenciais estão presentes
        essential_configs = ['[server]', '[theme]', 'headless = true']
        for config in essential_configs:
            if config not in config_content:
                print(f"❌ Configuração '{config}' não encontrada")
                return False
        
        print("✅ Configuração do Streamlit está correta")
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar configuração Streamlit: {e}")
        return False

def verificar_processamento_lotes():
    """Verifica se o processamento em lotes está implementado."""
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        # Verificar se as funções de lotes estão presentes
        funcoes_lotes = [
            'dividir_em_lotes',
            'process_file_in_batches',
            'total_produtos > 100',
            'Processar em Lotes'
        ]
        
        for funcao in funcoes_lotes:
            if funcao not in app_content:
                print(f"❌ Função '{funcao}' não encontrada em app.py")
                return False
        
        print("✅ Processamento em lotes implementado corretamente")
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar processamento em lotes: {e}")
        return False

def main():
    """Função principal de verificação."""
    print("🔍 Verificando projeto para deploy no Streamlit Cloud...")
    print("=" * 60)
    
    # Verificar arquivos necessários
    print("\n📁 Verificando arquivos necessários...")
    arquivos_faltando = verificar_arquivos_necessarios()
    if arquivos_faltando:
        print("❌ Arquivos faltando:")
        for arquivo in arquivos_faltando:
            print(f"   - {arquivo}")
        return False
    else:
        print("✅ Todos os arquivos necessários estão presentes")
    
    # Verificar imports
    print("\n📦 Verificando imports...")
    if not verificar_imports():
        return False
    
    # Verificar configuração
    print("\n⚙️ Verificando configuração...")
    if not verificar_configuracao():
        return False
    
    # Verificar requirements
    print("\n📋 Verificando requirements...")
    if not verificar_requirements():
        return False
    
    # Verificar configuração Streamlit
    print("\n🎨 Verificando configuração Streamlit...")
    if not verificar_streamlit_config():
        return False
    
    # Verificar processamento em lotes
    print("\n📦 Verificando processamento em lotes...")
    if not verificar_processamento_lotes():
        return False
    
    print("\n" + "=" * 60)
    print("🎉 PROJETO PRONTO PARA DEPLOY!")
    print("=" * 60)
    print("\n📋 Próximos passos:")
    print("1. Faça commit e push para o GitHub")
    print("2. Acesse share.streamlit.io")
    print("3. Configure as API Keys nas Secrets")
    print("4. Faça o deploy!")
    print("\n📖 Consulte o arquivo GUIA_DEPLOY_STREAMLIT_CLOUD.md para instruções detalhadas")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
