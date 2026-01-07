#!/usr/bin/env python3
"""
Interface Streamlit para o Melhorador de Descrições de Produtos com SEO.
Permite upload de arquivos Excel, configuração de parâmetros e acompanhamento do processamento.
"""

import streamlit as st
import pandas as pd
import os
import tempfile
import json
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import io
import sys
from contextlib import redirect_stdout, redirect_stderr
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Importar classes do módulo principal
from product_description_enhancer import (
    ProductDescriptionEnhancer, 
    OpenAIProvider, 
    ProductInfo,
    load_config,
    clean_product_title,
    filter_prohibited_content,
    remove_caixaria_numbers,
    get_dynamic_length_limits,
    ensure_description_length
)

# Configurar página
st.set_page_config(
    page_title="Melhorador de Descrições - Compra Agora",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .log-container {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1rem;
        max-height: 400px;
        overflow-y: auto;
        font-family: monospace;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

class StreamlitLogger:
    """Logger personalizado para Streamlit que captura logs em tempo real."""
    
    def __init__(self):
        self.logs = []
        self.logger = logging.getLogger('streamlit_app')
        self.logger.setLevel(logging.INFO)
        
        # Criar handler que adiciona logs à lista
        handler = logging.StreamHandler(io.StringIO())
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)
        self.string_io = io.StringIO()
    
    def info(self, message: str):
        """Adiciona log de informação."""
        self.logger.info(message)
        self.logs.append(f"[INFO] {message}")
    
    def warning(self, message: str):
        """Adiciona log de aviso."""
        self.logger.warning(message)
        self.logs.append(f"[WARNING] {message}")
    
    def error(self, message: str):
        """Adiciona log de erro."""
        self.logger.error(message)
        self.logs.append(f"[ERROR] {message}")
    
    def get_logs(self) -> str:
        """Retorna todos os logs como string."""
        return "\n".join(self.logs)
    
    def clear_logs(self):
        """Limpa todos os logs."""
        self.logs = []

class StreamlitProductEnhancer(ProductDescriptionEnhancer):
    """Versão do ProductDescriptionEnhancer adaptada para Streamlit."""
    
    def __init__(self, ai_provider, min_ratio: float = 1.5, config: Dict[str, Any] = None, 
                 streamlit_logger: Optional[StreamlitLogger] = None):
        super().__init__(ai_provider, min_ratio, config)
        self.streamlit_logger = streamlit_logger or StreamlitLogger()
        self.progress_bar = None
        self.status_text = None
    
    def set_progress_elements(self, progress_bar, status_text):
        """Define elementos de progresso do Streamlit."""
        self.progress_bar = progress_bar
        self.status_text = status_text
    
    def process_excel_file_streamlit(self, df: pd.DataFrame, column_mapping: Dict[str, str] = None) -> pd.DataFrame:
        """
        Processa DataFrame do Streamlit com feedback visual em tempo real.
        
        Args:
            df: DataFrame com dados dos produtos
            column_mapping: Mapeamento personalizado de colunas
            
        Returns:
            DataFrame processado com resultados
        """
        try:
            # Mapeamento padrão de colunas
            default_mapping = {
                'title': 'Título',
                'description': 'Descrição', 
                'price': 'Preço',
                'sku': 'SKU',
                'category': 'Categoria',
                'brand': 'Marca'
            }
            
            if column_mapping:
                default_mapping.update(column_mapping)
            
            # Verificar colunas necessárias
            required_columns = [default_mapping['title'], default_mapping['description']]
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"Colunas necessárias não encontradas: {missing_columns}")
            
            # Adicionar colunas de resultado
            df['Descrição_Melhorada'] = ''
            df['Status_Melhoria'] = ''
            df['Motivo_Melhoria'] = ''
            df['Razão_Título_Descrição'] = ''
            df['Meta_Title'] = ''
            df['Meta_Description'] = ''
            
            # Processar cada linha
            total_rows = len(df)
            self.streamlit_logger.info(f"Iniciando processamento de {total_rows} produtos...")
            
            # Usar enumerate para ter controle sequencial do índice
            for current_index, (original_index, row) in enumerate(df.iterrows()):
                try:
                    # Atualizar progresso usando índice sequencial
                    if self.progress_bar and hasattr(self.progress_bar, 'progress'):
                        try:
                            progress = (current_index + 1) / total_rows
                            # Garantir que o progresso esteja entre 0.0 e 1.0
                            progress = max(0.0, min(1.0, progress))
                            self.progress_bar.progress(progress)
                        except Exception as e:
                            # Se houver erro no progresso, apenas logar e continuar
                            self.streamlit_logger.warning(f"Erro ao atualizar progresso: {str(e)}")
                    
                    if self.status_text and hasattr(self.status_text, 'text'):
                        try:
                            self.status_text.text(f"Processando produto {current_index + 1}/{total_rows}")
                        except Exception as e:
                            # Se houver erro no status, apenas logar e continuar
                            self.streamlit_logger.warning(f"Erro ao atualizar status: {str(e)}")
                    
                    # Criar objeto do produto
                    product = self.create_product_info(row, default_mapping)
                    
                    # Limpar título para melhorar a geração de meta tags (igual ao comando manual)
                    product.title = clean_product_title(product.title)
                    
                    # Calcular razão título/descrição
                    title_length = len(product.title)
                    description_length = len(product.description)
                    ratio = description_length / title_length if title_length > 0 else 0
                    
                    df.at[original_index, 'Razão_Título_Descrição'] = f"{ratio:.2f}"
                    
                    # Verificar se deve melhorar
                    should_enhance, motivo = self.should_enhance_description(product.title, product.description)
                    df.at[original_index, 'Motivo_Melhoria'] = motivo
                    
                    if should_enhance:
                        self.streamlit_logger.info(f"Melhorando produto {current_index + 1}: {product.title[:50]}...")
                        
                        # Gerar conteúdo SEO completo (descrição + meta tags)
                        seo_info = self.ai_provider.generate_seo_content(product, self.config)
                        
                        # Verificar similaridade e tentar retries se necessário (igual ao comando manual)
                        enhanced = seo_info.enhanced_description or ""
                        if self._is_too_similar(enhanced, product.description):
                            self.streamlit_logger.warning("  Descrição melhorada muito similar à original. Tentando nova geração...")
                            max_retries = 2
                            for attempt in range(1, max_retries + 1):
                                time.sleep(0.5)
                                candidate = self.ai_provider.enhance_description(product, self.config) or ""
                                if not self._is_too_similar(candidate, product.description):
                                    enhanced = candidate
                                    self.streamlit_logger.info(f"  Nova variação aceita na tentativa {attempt}")
                                    break
                            else:
                                # Fallback baseado em regras para garantir mudança
                                self.streamlit_logger.warning("  Mantida alta similaridade após retries. Aplicando fallback baseado em regras.")
                                enhanced = self._generate_rule_based_description(product)
                        
                        # Filtrar conteúdo proibido (igual ao comando manual)
                        enhanced = filter_prohibited_content(enhanced, self.prohibited_phrases, self.config)
                        
                        # Remover números de caixaria (igual ao comando manual)
                        enhanced = remove_caixaria_numbers(enhanced)
                        
                        # Validar comprimento da descrição usando regras dinâmicas (igual ao comando manual)
                        min_chars, max_chars = get_dynamic_length_limits(product.description, self.config)
                        enhanced = ensure_description_length(enhanced, min_chars, max_chars)
                        
                        # Atualizar DataFrame com todas as informações
                        df.at[original_index, 'Descrição_Melhorada'] = enhanced
                        df.at[original_index, 'Meta_Title'] = seo_info.meta_title
                        df.at[original_index, 'Meta_Description'] = seo_info.meta_description
                        df.at[original_index, 'Status_Melhoria'] = 'MELHORADO'
                        
                        self.stats['enhanced'] += 1
                        
                    else:
                        self.streamlit_logger.info(f"Mantendo produto {current_index + 1}: {product.title[:50]}...")
                        
                        # Gerar apenas meta tags
                        seo_info = self.ai_provider.generate_seo_content(product, self.config)
                        
                        df.at[original_index, 'Descrição_Melhorada'] = product.description
                        df.at[original_index, 'Meta_Title'] = seo_info.meta_title
                        df.at[original_index, 'Meta_Description'] = seo_info.meta_description
                        df.at[original_index, 'Status_Melhoria'] = 'MANTIDO'
                        
                        self.stats['skipped'] += 1
                    
                    self.stats['total_processed'] += 1
                    
                    # Log de progresso a cada 5 produtos
                    if (current_index + 1) % 5 == 0:
                        self.streamlit_logger.info(f"Progresso: {current_index + 1}/{total_rows} produtos processados")
                
                except Exception as e:
                    self.streamlit_logger.error(f"Erro ao processar linha {current_index + 1}: {str(e)}")
                    df.at[original_index, 'Status_Melhoria'] = 'ERRO'
                    df.at[original_index, 'Descrição_Melhorada'] = product.description if 'product' in locals() else ''
                    df.at[original_index, 'Meta_Title'] = ''
                    df.at[original_index, 'Meta_Description'] = ''
                    self.stats['errors'] += 1
            
            # Estatísticas finais
            self.streamlit_logger.info(f"Processamento concluído!")
            self.streamlit_logger.info(f"Total processado: {self.stats['total_processed']}")
            self.streamlit_logger.info(f"Melhorados: {self.stats['enhanced']}")
            self.streamlit_logger.info(f"Mantidos: {self.stats['skipped']}")
            self.streamlit_logger.info(f"Erros: {self.stats['errors']}")
            
            return df
            
        except Exception as e:
            self.streamlit_logger.error(f"Erro ao processar arquivo: {str(e)}")
            raise

def main():
    """Função principal da aplicação Streamlit."""
    
    # Header principal
    st.markdown('<h1 class="main-header">🚀 Melhorador de Descrições de Produtos com SEO</h1>', unsafe_allow_html=True)
    
    # Sidebar para configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Campo para inserir API Key da OpenAI
        st.subheader("🔑 OpenAI API Key")
        
        # Tentar carregar do .env primeiro
        default_key = os.getenv('OPENAI_API_KEY', '')
        
        api_key = st.text_input(
            "Insira sua API Key da OpenAI",
            value=default_key,
            type="password",
            help="Você pode inserir a API Key aqui ou configurar no arquivo .env como OPENAI_API_KEY"
        )
        
        # Verificar se API Key foi fornecida
        if not api_key:
            st.error("❌ API Key da OpenAI é obrigatória")
            st.info("💡 Insira sua API Key acima ou configure OPENAI_API_KEY no arquivo .env")
            st.markdown("""
            **Como obter sua API Key:**
            1. Acesse https://platform.openai.com/api-keys
            2. Faça login na sua conta OpenAI
            3. Crie uma nova API Key
            4. Cole a chave no campo acima
            """)
            st.stop()
        else:
            st.success("✅ API Key configurada")
        
        # Modelo OpenAI
        model = st.selectbox(
            "Modelo OpenAI",
            ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
            index=0,
            help="Modelo específico da OpenAI a ser usado"
        )
        
        # Razão mínima
        min_ratio = st.slider(
            "Razão mínima descrição/título",
            min_value=1.0,
            max_value=3.0,
            value=1.5,
            step=0.1,
            help="Razão mínima entre tamanho da descrição e título para melhorar"
        )
        
        # Configurações avançadas
        with st.expander("🔧 Configurações Avançadas"):
            # Carregar configuração padrão
            config = load_config()
            prompt_settings = config.get('prompt_settings', {})
            
            # Temperature (controle de criatividade)
            temperature = st.slider(
                "Temperature (Criatividade)",
                min_value=0.0,
                max_value=1.0,
                value=prompt_settings.get('temperature', 0.7),
                step=0.1,
                help="Valores mais altos (0.8-1.0) = mais criativo. Valores mais baixos (0.0-0.3) = mais preciso e consistente"
            )
            
            # Max tokens
            max_tokens = st.number_input(
                "Max Tokens (Tamanho máximo da resposta)",
                min_value=100,
                max_value=2000,
                value=prompt_settings.get('max_tokens', 500),
                step=50,
                help="Número máximo de tokens na resposta da IA (1 token ≈ 4 caracteres)"
            )
            
            # Frases proibidas
            default_prohibited = "\n".join(config.get('prohibited_phrases', [
                "margem", "lucro", "margem de lucro", "clientes frescos"
            ]))
            prohibited_phrases = st.text_area(
                "Frases proibidas (uma por linha)",
                value=default_prohibited,
                help="Frases que não devem aparecer nas descrições geradas"
            )
            
            # Configurações de comprimento
            desc_length = config.get('description_length', {})
            short_desc = desc_length.get('short_description', {})
            long_desc = desc_length.get('long_description', {})
            
            min_chars = st.number_input(
                "Mínimo de caracteres",
                min_value=100,
                max_value=500,
                value=short_desc.get('min_chars', 300),
                help="Comprimento mínimo da descrição melhorada"
            )
            
            max_chars = st.number_input(
                "Máximo de caracteres",
                min_value=300,
                max_value=1000,
                value=long_desc.get('max_chars', 450),
                help="Comprimento máximo da descrição melhorada"
            )
            
            # Mapeamento de colunas personalizado
            st.subheader("📋 Mapeamento de Colunas (Opcional)")
            st.info("💡 Use apenas se seu arquivo Excel tiver nomes de colunas diferentes dos padrões")
            
            col_mapping = config.get('column_mapping', {})
            
            col_title = st.text_input(
                "Nome da coluna 'Título'",
                value=col_mapping.get('title', 'Título'),
                help="Nome exato da coluna que contém o título do produto"
            )
            
            col_description = st.text_input(
                "Nome da coluna 'Descrição'",
                value=col_mapping.get('description', 'Descrição'),
                help="Nome exato da coluna que contém a descrição do produto"
            )
            
            col_price = st.text_input(
                "Nome da coluna 'Preço' (opcional)",
                value=col_mapping.get('price', 'Preço'),
                help="Nome da coluna de preço (deixe vazio se não houver)"
            )
            
            col_sku = st.text_input(
                "Nome da coluna 'SKU' (opcional)",
                value=col_mapping.get('sku', 'SKU'),
                help="Nome da coluna de SKU (deixe vazio se não houver)"
            )
            
            col_category = st.text_input(
                "Nome da coluna 'Categoria' (opcional)",
                value=col_mapping.get('category', 'Categoria'),
                help="Nome da coluna de categoria (deixe vazio se não houver)"
            )
            
            col_brand = st.text_input(
                "Nome da coluna 'Marca' (opcional)",
                value=col_mapping.get('brand', 'Marca'),
                help="Nome da coluna de marca (deixe vazio se não houver)"
            )
            
            # Criar dicionário de mapeamento
            column_mapping = {
                'title': col_title if col_title else 'Título',
                'description': col_description if col_description else 'Descrição',
            }
            if col_price:
                column_mapping['price'] = col_price
            if col_sku:
                column_mapping['sku'] = col_sku
            if col_category:
                column_mapping['category'] = col_category
            if col_brand:
                column_mapping['brand'] = col_brand
    
    # Área principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 Upload do Arquivo")
        
        # Upload de arquivo
        uploaded_file = st.file_uploader(
            "Escolha um arquivo Excel (.xlsx)",
            type=['xlsx', 'xls'],
            help="Arquivo deve conter colunas: Título, Descrição, Preço, SKU, Categoria, Marca"
        )
        
        if uploaded_file is not None:
            try:
                # Ler arquivo
                df = pd.read_excel(uploaded_file)
                total_produtos = len(df)
                
                st.success(f"✅ Arquivo carregado com sucesso! {total_produtos} produtos encontrados.")
                
                # Verificar se é um arquivo grande
                if total_produtos > 50:
                    st.warning(f"⚠️ Arquivo grande detectado: {total_produtos} produtos")
                    
                    # Calcular lotes otimizados baseado no tamanho
                    if total_produtos <= 200:
                        tamanho_lote_recomendado = 50
                        tempo_estimado = total_produtos * 0.3  # 0.3 min por produto
                    elif total_produtos <= 500:
                        tamanho_lote_recomendado = 50
                        tempo_estimado = total_produtos * 0.3
                    else:  # 500+ produtos
                        tamanho_lote_recomendado = 25
                        tempo_estimado = total_produtos * 0.4
                    
                    lotes_necessarios = (total_produtos + tamanho_lote_recomendado - 1) // tamanho_lote_recomendado
                    
                    st.info(f"💡 Recomendamos processar em lotes de {tamanho_lote_recomendado} produtos")
                    st.info(f"📊 Serão necessários {lotes_necessarios} lotes")
                    st.info(f"⏱️ Tempo estimado: {tempo_estimado:.0f} minutos")
                    
                    # Opções de processamento
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        processar_lotes_pequenos = st.button(f"📦 Lotes de {tamanho_lote_recomendado} (Recomendado)", type="primary")
                    
                    with col2:
                        processar_lotes_100 = st.button("📦 Lotes de 100 (Mais Rápido)", type="secondary")
                    
                    with col3:
                        processar_tudo = st.button("⚡ Processar Tudo (Risco Alto)", type="secondary")
                    
                    if processar_lotes_pequenos:
                        process_file_in_batches(df, api_key, model, min_ratio, prohibited_phrases, min_chars, max_chars, temperature, max_tokens, column_mapping, tamanho_lote_recomendado)
                    elif processar_lotes_100:
                        process_file_in_batches(df, api_key, model, min_ratio, prohibited_phrases, min_chars, max_chars, temperature, max_tokens, column_mapping, 100)
                    elif processar_tudo:
                        st.warning("⚠️ Processando todos os produtos de uma vez. Risco muito alto de timeout!")
                        process_file(df, api_key, model, min_ratio, prohibited_phrases, min_chars, max_chars, temperature, max_tokens, column_mapping)
                else:
                    # Arquivo pequeno, processar normalmente
                    st.success(f"✅ Arquivo pequeno: {total_produtos} produtos")
                    
                    # Mostrar preview dos dados
                    with st.expander("👀 Preview dos Dados"):
                        st.dataframe(df.head(10))
                    
                    # Botão para processar
                    if st.button("🚀 Processar Arquivo", type="primary"):
                        process_file(df, api_key, model, min_ratio, prohibited_phrases, min_chars, max_chars, temperature, max_tokens, column_mapping)
                
                # Verificar colunas necessárias
                required_columns = ['Título', 'Descrição']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    st.error(f"❌ Colunas necessárias não encontradas: {missing_columns}")
                    st.info("💡 O arquivo deve conter pelo menos as colunas 'Título' e 'Descrição'")
                            
            except Exception as e:
                st.error(f"❌ Erro ao ler arquivo: {str(e)}")
    
    with col2:
        st.header("📊 Informações")
        
        st.info("""
        **Como usar:**
        
        1. Configure API Key no arquivo .env
        2. Faça upload do arquivo Excel
        3. Ajuste as configurações
        4. Clique em "Processar Arquivo"
        5. Acompanhe o progresso
        6. Baixe o resultado
        
        **Colunas necessárias:**
        - Título
        - Descrição
        - Preço (opcional)
        - SKU (opcional)
        - Categoria (opcional)
        - Marca (opcional)
        """)
        
        # Status da aplicação
        st.header("🔍 Status")
        
        if 'processing' not in st.session_state:
            st.session_state.processing = False
        
        if st.session_state.processing:
            st.warning("⏳ Processando...")
        else:
            st.success("✅ Pronto para processar")

def processar_lote_simples(lote: pd.DataFrame, ai_provider, min_ratio: float, config: Dict[str, Any], 
                          streamlit_logger: StreamlitLogger, numero_lote: int, total_lotes: int) -> pd.DataFrame:
    """
    Processa um lote sem usar elementos de UI do Streamlit para evitar conflitos.
    """
    try:
        # Usar mapeamento do config ou padrão
        default_mapping = config.get('column_mapping', {
            'title': 'Título',
            'description': 'Descrição', 
            'price': 'Preço',
            'sku': 'SKU',
            'category': 'Categoria',
            'brand': 'Marca'
        })
        
        # Adicionar colunas de resultado
        lote['Descrição_Melhorada'] = ''
        lote['Status_Melhoria'] = ''
        lote['Motivo_Melhoria'] = ''
        lote['Razão_Título_Descrição'] = ''
        lote['Meta_Title'] = ''
        lote['Meta_Description'] = ''
        
        # Processar cada linha
        total_rows = len(lote)
        streamlit_logger.info(f"Processando lote {numero_lote}/{total_lotes}: {total_rows} produtos")
        
        for current_index, (original_index, row) in enumerate(lote.iterrows()):
            try:
                # Criar objeto do produto
                product = ProductInfo(
                    title=str(row.get(default_mapping.get('title', 'title'), '')).strip(),
                    description=str(row.get(default_mapping.get('description', 'description'), '')).strip(),
                    price=str(row.get(default_mapping.get('price', 'price'), '')).strip(),
                    sku=str(row.get(default_mapping.get('sku', 'sku'), '')).strip(),
                    category=str(row.get(default_mapping.get('category', 'category'), '')).strip(),
                    brand=str(row.get(default_mapping.get('brand', 'brand'), '')).strip()
                )
                
                # Limpar título para melhorar a geração de meta tags (igual ao comando manual)
                product.title = clean_product_title(product.title)
                
                # Calcular razão título/descrição
                title_length = len(product.title)
                description_length = len(product.description)
                ratio = description_length / title_length if title_length > 0 else 0
                
                lote.at[original_index, 'Razão_Título_Descrição'] = f"{ratio:.2f}"
                
                # Verificar se deve melhorar
                should_enhance, motivo = True, "Sempre melhorar com base no retorno da IA"
                lote.at[original_index, 'Motivo_Melhoria'] = motivo
                
                if should_enhance:
                    streamlit_logger.info(f"Lote {numero_lote} - Melhorando produto {current_index + 1}: {product.title[:50]}...")
                    
                    # Gerar conteúdo SEO completo (descrição + meta tags)
                    seo_info = ai_provider.generate_seo_content(product, config)
                    
                    # Verificar similaridade e tentar retries se necessário (igual ao comando manual)
                    enhanced = seo_info.enhanced_description or ""
                    # Criar instância temporária para usar métodos da classe
                    temp_enhancer = ProductDescriptionEnhancer(ai_provider, 1.5, config)
                    if temp_enhancer._is_too_similar(enhanced, product.description):
                        streamlit_logger.warning(f"  Descrição melhorada muito similar à original. Tentando nova geração...")
                        max_retries = 2
                        for attempt in range(1, max_retries + 1):
                            time.sleep(0.5)
                            candidate = ai_provider.enhance_description(product, config) or ""
                            if not temp_enhancer._is_too_similar(candidate, product.description):
                                enhanced = candidate
                                streamlit_logger.info(f"  Nova variação aceita na tentativa {attempt}")
                                break
                        else:
                            # Fallback baseado em regras para garantir mudança
                            streamlit_logger.warning("  Mantida alta similaridade após retries. Aplicando fallback baseado em regras.")
                            enhanced = temp_enhancer._generate_rule_based_description(product)
                    
                    # Filtrar conteúdo proibido (igual ao comando manual)
                    prohibited_phrases = config.get('prohibited_phrases', [])
                    enhanced = filter_prohibited_content(enhanced, prohibited_phrases, config)
                    
                    # Remover números de caixaria (igual ao comando manual)
                    enhanced = remove_caixaria_numbers(enhanced)
                    
                    # Validar comprimento da descrição usando regras dinâmicas (igual ao comando manual)
                    min_chars, max_chars = get_dynamic_length_limits(product.description, config)
                    enhanced = ensure_description_length(enhanced, min_chars, max_chars)
                    
                    # Atualizar DataFrame com todas as informações
                    lote.at[original_index, 'Descrição_Melhorada'] = enhanced
                    lote.at[original_index, 'Meta_Title'] = seo_info.meta_title
                    lote.at[original_index, 'Meta_Description'] = seo_info.meta_description
                    lote.at[original_index, 'Status_Melhoria'] = 'MELHORADO'
                    
                else:
                    streamlit_logger.info(f"Lote {numero_lote} - Mantendo produto {current_index + 1}: {product.title[:50]}...")
                    
                    # Gerar apenas meta tags (mesmo quando mantém descrição, gera meta tags)
                    seo_info = ai_provider.generate_seo_content(product, config)
                    
                    lote.at[original_index, 'Descrição_Melhorada'] = product.description
                    lote.at[original_index, 'Meta_Title'] = seo_info.meta_title
                    lote.at[original_index, 'Meta_Description'] = seo_info.meta_description
                    lote.at[original_index, 'Status_Melhoria'] = 'MANTIDO'
                
                # Log de progresso a cada 5 produtos
                if (current_index + 1) % 5 == 0:
                    streamlit_logger.info(f"Lote {numero_lote} - Progresso: {current_index + 1}/{total_rows} produtos processados")
            
            except Exception as e:
                streamlit_logger.error(f"Lote {numero_lote} - Erro ao processar linha {current_index + 1}: {str(e)}")
                lote.at[original_index, 'Status_Melhoria'] = 'ERRO'
                lote.at[original_index, 'Descrição_Melhorada'] = product.description if 'product' in locals() else ''
                lote.at[original_index, 'Meta_Title'] = ''
                lote.at[original_index, 'Meta_Description'] = ''
        
        streamlit_logger.info(f"Lote {numero_lote} concluído com sucesso!")
        return lote
        
    except Exception as e:
        streamlit_logger.error(f"Erro ao processar lote {numero_lote}: {str(e)}")
        # Retornar lote com erro
        lote['Status_Melhoria'] = 'ERRO'
        lote['Descrição_Melhorada'] = lote['Descrição']
        lote['Meta_Title'] = ''
        lote['Meta_Description'] = ''
        return lote

def dividir_em_lotes(df: pd.DataFrame, tamanho_lote: int = 100):
    """
    Divide um DataFrame em lotes menores.
    
    Args:
        df: DataFrame com todos os produtos
        tamanho_lote: Tamanho de cada lote (padrão: 100)
        
    Returns:
        Lista de DataFrames, cada um representando um lote
    """
    lotes = []
    total_produtos = len(df)
    
    for i in range(0, total_produtos, tamanho_lote):
        lote = df.iloc[i:i + tamanho_lote].copy()
        lotes.append(lote)
    
    return lotes

def process_file_in_batches(df: pd.DataFrame, api_key: str, model: str, 
                          min_ratio: float, prohibited_phrases: str, min_chars: int, max_chars: int, tamanho_lote: int = 50):
    """
    Processa arquivo em lotes otimizados para evitar timeouts no Streamlit Cloud.
    """
    # Configurar estado
    st.session_state.processing = True
    
    # Criar logger personalizado
    streamlit_logger = StreamlitLogger()
    
    try:
        # Configurar configuração personalizada
        config = {
            'prohibited_phrases': [phrase.strip() for phrase in prohibited_phrases.split('\n') if phrase.strip()],
            'description_length': {
                'min_chars': min_chars,
                'max_chars': max_chars
            },
            'prompt_settings': {
                'temperature': temperature,
                'max_tokens': max_tokens
            },
            'column_mapping': column_mapping
        }
        
        # Criar provedor de IA (OpenAI)
        ai_provider = OpenAIProvider(api_key, model)
        
        # Dividir em lotes otimizados
        lotes = dividir_em_lotes(df, tamanho_lote)
        total_lotes = len(lotes)
        
        st.header("📦 Processamento em Lotes Otimizado")
        st.info(f"📊 Arquivo dividido em {total_lotes} lotes de {tamanho_lote} produtos cada")
        
        # Calcular tempo estimado mais preciso e otimizado
        if model == "gpt-3.5-turbo":
            tempo_por_produto = 0.15  # Mais rápido
        elif model == "gpt-4":
            tempo_por_produto = 0.3   # Mais lento
        else:  # gpt-4-turbo
            tempo_por_produto = 0.25  # Balanceado
        
        tempo_estimado_total = len(df) * tempo_por_produto
        
        # Avisar se o tempo estimado é muito longo
        if tempo_estimado_total > 8:  # Mais de 8 minutos
            st.warning(f"⚠️ Tempo estimado muito longo: {tempo_estimado_total:.0f} minutos")
            st.info("💡 Recomendamos usar lotes menores ou modelo mais rápido (gpt-3.5-turbo)")
        
        st.info(f"⏱️ Tempo estimado total: {tempo_estimado_total:.0f} minutos")
        st.info(f"🚀 Usando modelo: {model} (OpenAI)")
        
        # Mostrar informações dos lotes
        with st.expander("📋 Informações dos Lotes"):
            for i, lote in enumerate(lotes, 1):
                inicio = lote.index[0] + 1
                fim = lote.index[-1] + 1
                tempo_lote = len(lote) * tempo_por_produto
                st.write(f"**Lote {i}**: Produtos {inicio} a {fim} ({len(lote)} produtos) - ~{tempo_lote:.1f} min")
        
        # Processar cada lote com melhor controle de timeout
        resultados = []
        tempo_inicio_total = time.time()
        
        for i, lote in enumerate(lotes, 1):
            st.subheader(f"🔄 Processando Lote {i}/{total_lotes}")
            
            # Verificar tempo restante (Streamlit Cloud tem limite de 10 min)
            tempo_decorrido = time.time() - tempo_inicio_total
            tempo_restante_estimado = (total_lotes - i + 1) * len(lote) * tempo_por_produto * 60
            
            # Limite mais conservador para evitar timeout
            if tempo_decorrido > 360:  # 6 minutos (deixar margem de 4 min)
                st.warning("⚠️ Tempo limite próximo! Salvando progresso atual...")
                
                # Mostrar estatísticas do que foi processado
                produtos_processados = sum(len(resultado) for resultado in resultados)
                st.info(f"📊 Produtos processados até agora: {produtos_processados}")
                st.info(f"📊 Lotes concluídos: {len(resultados)}/{total_lotes}")
                
                # Salvar resultado parcial
                if resultados:
                    st.subheader("💾 Salvando Resultado Parcial")
                    resultado_parcial = pd.concat(resultados, ignore_index=True)
                    
                    # Criar arquivo Excel em memória
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        resultado_parcial.to_excel(writer, index=False, sheet_name='Resultados_Parciais')
                    
                    output.seek(0)
                    
                    st.download_button(
                        label="📥 Baixar Resultado Parcial",
                        data=output.getvalue(),
                        file_name=f"produtos_processados_parcial_{int(time.time())}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                    st.success(f"✅ {len(resultado_parcial)} produtos processados com sucesso!")
                    st.info("💡 Para processar o restante, faça upload novamente do arquivo original e processe os lotes restantes.")
                
                break
            
            # Criar melhorador para este lote
            enhancer = StreamlitProductEnhancer(ai_provider, min_ratio, config, streamlit_logger)
            
            # Área de progresso do lote (criar novos elementos para cada lote)
            progress_bar = st.progress(0)
            status_text = st.empty()
            enhancer.set_progress_elements(progress_bar, status_text)
            
            # Limpar estado anterior do enhancer
            enhancer.stats = {
                'total_processed': 0,
                'enhanced': 0,
                'skipped': 0,
                'errors': 0
            }
            
            # Processar lote com timeout interno
            try:
                with st.spinner(f"Processando lote {i}... (Tempo restante: ~{tempo_restante_estimado/60:.1f} min)"):
                    # Processar lote usando método mais simples para evitar conflitos de UI
                    lote_resultado = processar_lote_simples(lote, ai_provider, min_ratio, config, streamlit_logger, i, total_lotes)
                    resultados.append(lote_resultado)
                
                st.success(f"✅ Lote {i} concluído! {len(lote_resultado)} produtos processados")
                
                # Pausa otimizada entre lotes (reduzida para acelerar)
                if i < total_lotes:
                    pausa = 1 if tamanho_lote <= 25 else 2  # Pausa muito menor
                    st.info(f"⏳ Aguardando {pausa} segundo(s) antes do próximo lote...")
                    time.sleep(pausa)
                    
                    # Limpar elementos de UI para evitar conflitos
                    st.empty()
                    
            except Exception as e:
                st.error(f"❌ Erro no lote {i}: {str(e)}")
                st.warning("⚠️ Continuando com o próximo lote...")
                # Adicionar lote com erro para manter a estrutura
                lote_erro = lote.copy()
                lote_erro['Status_Melhoria'] = 'ERRO'
                lote_erro['Descrição_Melhorada'] = lote_erro['Descrição']
                lote_erro['Meta_Title'] = ''
                lote_erro['Meta_Description'] = ''
                resultados.append(lote_erro)
        
        # Combinar resultados
        if resultados:
            st.subheader("📋 Combinando Resultados")
            resultado_final = pd.concat(resultados, ignore_index=True)
            
            st.success(f"🎉 Processamento concluído! {len(resultado_final)} produtos processados")
            
            # Mostrar estatísticas finais
            st.header("📊 Estatísticas Finais")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Processado", len(resultado_final))
            
            with col2:
                melhorados = len(resultado_final[resultado_final['Status_Melhoria'] == 'MELHORADO'])
                st.metric("Melhorados", melhorados)
            
            with col3:
                mantidos = len(resultado_final[resultado_final['Status_Melhoria'] == 'MANTIDO'])
                st.metric("Mantidos", mantidos)
            
            with col4:
                erros = len(resultado_final[resultado_final['Status_Melhoria'] == 'ERRO'])
                st.metric("Erros", erros)
            
            # Mostrar resultados
            st.header("📋 Resultados")
            
            # Filtros para visualização
            col1, col2 = st.columns(2)
            
            with col1:
                status_filter = st.selectbox(
                    "Filtrar por status",
                    ["Todos", "MELHORADO", "MANTIDO", "ERRO"]
                )
            
            with col2:
                show_columns = st.multiselect(
                    "Colunas para mostrar",
                    ["Título", "Descrição", "Descrição_Melhorada", "Meta_Title", "Meta_Description", "Status_Melhoria"],
                    default=["Título", "Descrição_Melhorada", "Meta_Title", "Meta_Description", "Status_Melhoria"]
                )
            
            # Aplicar filtros
            if status_filter != "Todos":
                filtered_df = resultado_final[resultado_final['Status_Melhoria'] == status_filter]
            else:
                filtered_df = resultado_final
            
            # Mostrar tabela
            if show_columns:
                st.dataframe(filtered_df[show_columns], use_container_width=True)
            
            # Botão para download
            st.header("💾 Download dos Resultados")
            
            # Criar arquivo Excel em memória
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                resultado_final.to_excel(writer, index=False, sheet_name='Resultados')
            
            output.seek(0)
            
            st.download_button(
                label="📥 Baixar Arquivo Processado",
                data=output.getvalue(),
                file_name=f"produtos_melhorados_lotes_{int(time.time())}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("❌ Nenhum lote foi processado com sucesso.")
        
    except Exception as e:
        st.error(f"❌ Erro durante o processamento em lotes: {str(e)}")
        streamlit_logger.error(f"Erro: {str(e)}")
        
        # Mostrar logs de erro
        st.markdown(f"""
        <div class="log-container">
        {streamlit_logger.get_logs().replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
    
    finally:
        # Resetar estado
        st.session_state.processing = False

def process_file(df: pd.DataFrame, api_key: str, model: str, 
                min_ratio: float, prohibited_phrases: str, min_chars: int, max_chars: int,
                temperature: float, max_tokens: int, column_mapping: dict):
    """Processa o arquivo com feedback visual."""
    
    # Configurar estado
    st.session_state.processing = True
    
    # Criar logger personalizado
    streamlit_logger = StreamlitLogger()
    
    try:
        # Configurar configuração personalizada
        config = {
            'prohibited_phrases': [phrase.strip() for phrase in prohibited_phrases.split('\n') if phrase.strip()],
            'description_length': {
                'min_chars': min_chars,
                'max_chars': max_chars
            },
            'prompt_settings': {
                'temperature': temperature,
                'max_tokens': max_tokens
            },
            'column_mapping': column_mapping
        }
        
        # Criar provedor de IA (OpenAI)
        ai_provider = OpenAIProvider(api_key, model)
        
        # Criar melhorador
        enhancer = StreamlitProductEnhancer(ai_provider, min_ratio, config, streamlit_logger)
        
        # Área de progresso
        st.header("📈 Progresso do Processamento")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        enhancer.set_progress_elements(progress_bar, status_text)
        
        # Área de logs
        st.header("📝 Logs em Tempo Real")
        log_container = st.empty()
        
        # Processar arquivo
        with st.spinner("Processando produtos..."):
            result_df = enhancer.process_excel_file_streamlit(df, column_mapping)
        
        # Atualizar logs finais
        log_container.markdown(f"""
        <div class="log-container">
        {streamlit_logger.get_logs().replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar estatísticas
        st.header("📊 Estatísticas do Processamento")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Processado", enhancer.stats['total_processed'])
        
        with col2:
            st.metric("Melhorados", enhancer.stats['enhanced'])
        
        with col3:
            st.metric("Mantidos", enhancer.stats['skipped'])
        
        with col4:
            st.metric("Erros", enhancer.stats['errors'])
        
        # Mostrar resultados
        st.header("📋 Resultados")
        
        # Filtros para visualização
        col1, col2 = st.columns(2)
        
        with col1:
            status_filter = st.selectbox(
                "Filtrar por status",
                ["Todos", "MELHORADO", "MANTIDO", "ERRO"]
            )
        
        with col2:
            show_columns = st.multiselect(
                "Colunas para mostrar",
                ["Título", "Descrição", "Descrição_Melhorada", "Meta_Title", "Meta_Description", "Status_Melhoria"],
                default=["Título", "Descrição_Melhorada", "Meta_Title", "Meta_Description", "Status_Melhoria"]
            )
        
        # Aplicar filtros
        if status_filter != "Todos":
            filtered_df = result_df[result_df['Status_Melhoria'] == status_filter]
        else:
            filtered_df = result_df
        
        # Mostrar tabela
        if show_columns:
            st.dataframe(filtered_df[show_columns], use_container_width=True)
        
        # Botão para download
        st.header("💾 Download dos Resultados")
        
        # Criar arquivo Excel em memória
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            result_df.to_excel(writer, index=False, sheet_name='Resultados')
        
        output.seek(0)
        
        st.download_button(
            label="📥 Baixar Arquivo Processado",
            data=output.getvalue(),
            file_name=f"produtos_melhorados_{int(time.time())}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.success("✅ Processamento concluído com sucesso!")
        
    except Exception as e:
        st.error(f"❌ Erro durante o processamento: {str(e)}")
        streamlit_logger.error(f"Erro: {str(e)}")
        
        # Mostrar logs de erro
        st.markdown(f"""
        <div class="log-container">
        {streamlit_logger.get_logs().replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
    
    finally:
        # Resetar estado
        st.session_state.processing = False

if __name__ == "__main__":
    main()
