#!/usr/bin/env python3
"""
Configurações específicas para o Streamlit Cloud.
Este arquivo contém configurações otimizadas para produção.
"""

import os
import streamlit as st
from typing import Dict, Any

def get_streamlit_config() -> Dict[str, Any]:
    """
    Retorna configurações otimizadas para Streamlit Cloud.
    
    Returns:
        Dict com configurações específicas para produção
    """
    return {
        # Configurações de performance
        'max_file_size_mb': 50,  # Limite de 50MB para arquivos
        'max_products_per_batch': 100,  # Máximo 100 produtos por lote (recomendado para Streamlit Cloud)
        'timeout_seconds': 300,  # Timeout de 5 minutos
        'batch_processing_enabled': True,  # Habilitar processamento em lotes
        'auto_split_large_files': True,  # Dividir automaticamente arquivos grandes
        
        # Configurações de IA
        'default_model_openai': 'gpt-3.5-turbo',  # Modelo mais rápido
        'default_model_gemini': 'gemini-pro',
        'max_tokens': 500,  # Limite de tokens para evitar custos altos
        'temperature': 0.7,
        
        # Configurações de cache
        'cache_ttl': 3600,  # Cache por 1 hora
        'enable_cache': True,
        
        # Configurações de UI
        'show_advanced_options': False,  # Ocultar opções avançadas por padrão
        'enable_dark_mode': False,
        'sidebar_collapsed': False,
        
        # Configurações de logging
        'log_level': 'INFO',
        'enable_file_logging': False,  # Desabilitar logs em arquivo no cloud
        'max_log_entries': 1000,
        
        # Configurações de segurança
        'enable_cors': False,
        'enable_xsrf_protection': True,
        'max_upload_size': 50 * 1024 * 1024,  # 50MB
        
        # Configurações específicas do Compra Agora
        'compra_agora_rules': {
            'meta_title_suffix': '- Compra Agora',
            'meta_title_max_length': 60,
            'meta_description_max_length': 160,
            'mandatory_brand_in_title': True,
            'keyword_position': 'inicio'
        }
    }

def validate_environment() -> bool:
    """
    Valida se o ambiente está configurado corretamente.
    
    Returns:
        True se tudo estiver OK, False caso contrário
    """
    # Verificar se estamos no Streamlit Cloud
    is_streamlit_cloud = os.getenv('STREAMLIT_CLOUD', 'false').lower() == 'true'
    
    # Verificar API Keys
    has_openai_key = bool(os.getenv('OPENAI_API_KEY'))
    has_gemini_key = bool(os.getenv('GEMINI_API_KEY'))
    
    # Pelo menos uma API Key deve estar configurada
    has_valid_api_key = has_openai_key or has_gemini_key
    
    return {
        'is_streamlit_cloud': is_streamlit_cloud,
        'has_openai_key': has_openai_key,
        'has_gemini_key': has_gemini_key,
        'has_valid_api_key': has_valid_api_key,
        'environment_ok': has_valid_api_key
    }

def get_optimized_model_config(provider: str) -> Dict[str, Any]:
    """
    Retorna configurações otimizadas de modelo para cada provedor.
    
    Args:
        provider: 'openai' ou 'gemini'
        
    Returns:
        Dict com configurações do modelo
    """
    configs = {
        'openai': {
            'model': 'gpt-3.5-turbo',
            'max_tokens': 500,
            'temperature': 0.7,
            'timeout': 30,
            'retry_attempts': 3
        },
        'gemini': {
            'model': 'gemini-pro',
            'max_tokens': 500,
            'temperature': 0.7,
            'timeout': 30,
            'retry_attempts': 3
        }
    }
    
    return configs.get(provider, configs['openai'])

def setup_streamlit_page_config():
    """
    Configura a página do Streamlit com otimizações para produção.
    """
    st.set_page_config(
        page_title="Melhorador de Descrições - Compra Agora",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://docs.streamlit.io/',
            'Report a bug': 'https://github.com/compra-agora-osf/issues',
            'About': 'Melhorador de Descrições com SEO para e-commerce'
        }
    )

def get_environment_info() -> Dict[str, str]:
    """
    Retorna informações sobre o ambiente de execução.
    
    Returns:
        Dict com informações do ambiente
    """
    return {
        'platform': os.getenv('PLATFORM', 'unknown'),
        'python_version': os.sys.version,
        'streamlit_version': st.__version__,
        'is_cloud': os.getenv('STREAMLIT_CLOUD', 'false'),
        'memory_limit': os.getenv('MEMORY_LIMIT', 'unknown'),
        'cpu_count': str(os.cpu_count())
    }

# Configurações globais
STREAMLIT_CONFIG = get_streamlit_config()
ENVIRONMENT_INFO = get_environment_info()
