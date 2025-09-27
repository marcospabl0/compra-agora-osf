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
    GeminiProvider,
    ProductInfo,
    load_config
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
            
            for index, row in df.iterrows():
                try:
                    # Atualizar progresso
                    if self.progress_bar:
                        progress = (index + 1) / total_rows
                        self.progress_bar.progress(progress)
                    
                    if self.status_text:
                        self.status_text.text(f"Processando produto {index + 1}/{total_rows}")
                    
                    # Criar objeto do produto
                    product = self.create_product_info(row, default_mapping)
                    
                    # Calcular razão título/descrição
                    title_length = len(product.title)
                    description_length = len(product.description)
                    ratio = description_length / title_length if title_length > 0 else 0
                    
                    df.at[index, 'Razão_Título_Descrição'] = f"{ratio:.2f}"
                    
                    # Verificar se deve melhorar
                    should_enhance, motivo = self.should_enhance_description(product.title, product.description)
                    df.at[index, 'Motivo_Melhoria'] = motivo
                    
                    if should_enhance:
                        self.streamlit_logger.info(f"Melhorando produto {index + 1}: {product.title[:50]}...")
                        
                        # Gerar conteúdo SEO completo
                        seo_info = self.ai_provider.generate_seo_content(product, self.config)
                        
                        # Atualizar DataFrame
                        df.at[index, 'Descrição_Melhorada'] = seo_info.enhanced_description
                        df.at[index, 'Meta_Title'] = seo_info.meta_title
                        df.at[index, 'Meta_Description'] = seo_info.meta_description
                        df.at[index, 'Status_Melhoria'] = 'MELHORADO'
                        
                        self.stats['enhanced'] += 1
                        
                    else:
                        self.streamlit_logger.info(f"Mantendo produto {index + 1}: {product.title[:50]}...")
                        
                        # Gerar apenas meta tags
                        seo_info = self.ai_provider.generate_seo_content(product, self.config)
                        
                        df.at[index, 'Descrição_Melhorada'] = product.description
                        df.at[index, 'Meta_Title'] = seo_info.meta_title
                        df.at[index, 'Meta_Description'] = seo_info.meta_description
                        df.at[index, 'Status_Melhoria'] = 'MANTIDO'
                        
                        self.stats['skipped'] += 1
                    
                    self.stats['total_processed'] += 1
                    
                    # Log de progresso a cada 5 produtos
                    if (index + 1) % 5 == 0:
                        self.streamlit_logger.info(f"Progresso: {index + 1}/{total_rows} produtos processados")
                
                except Exception as e:
                    self.streamlit_logger.error(f"Erro ao processar linha {index + 1}: {str(e)}")
                    df.at[index, 'Status_Melhoria'] = 'ERRO'
                    df.at[index, 'Descrição_Melhorada'] = product.description if 'product' in locals() else ''
                    df.at[index, 'Meta_Title'] = ''
                    df.at[index, 'Meta_Description'] = ''
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
        
        # Verificar API Keys disponíveis
        openai_key = os.getenv('OPENAI_API_KEY')
        gemini_key = os.getenv('GEMINI_API_KEY')
        
        # Mostrar status das API Keys
        st.subheader("🔑 Status das API Keys")
        
        col1, col2 = st.columns(2)
        with col1:
            if openai_key:
                st.success("✅ OpenAI")
            else:
                st.error("❌ OpenAI")
        
        with col2:
            if gemini_key:
                st.success("✅ Gemini")
            else:
                st.error("❌ Gemini")
        
        # Provedor de IA
        available_providers = []
        if openai_key:
            available_providers.append("openai")
        if gemini_key:
            available_providers.append("gemini")
        
        if not available_providers:
            st.error("❌ Nenhuma API Key configurada no arquivo .env")
            st.info("💡 Configure OPENAI_API_KEY ou GEMINI_API_KEY no arquivo .env")
            return
        
        provider = st.selectbox(
            "Provedor de IA",
            available_providers,
            help="Escolha entre OpenAI GPT ou Google Gemini"
        )
        
        # Obter API Key baseada no provedor selecionado
        api_key = openai_key if provider == "openai" else gemini_key
        
        # Modelo
        model_options = {
            "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
            "gemini": ["gemini-pro", "gemini-pro-vision"]
        }
        
        model = st.selectbox(
            "Modelo",
            model_options[provider],
            help="Modelo específico a ser usado"
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
            # Frases proibidas
            prohibited_phrases = st.text_area(
                "Frases proibidas (uma por linha)",
                value="margem\nlucro\nmargem de lucro\nclientes frescos",
                help="Frases que não devem aparecer nas descrições geradas"
            )
            
            # Configurações de comprimento
            min_chars = st.number_input(
                "Mínimo de caracteres",
                min_value=100,
                max_value=500,
                value=300,
                help="Comprimento mínimo da descrição melhorada"
            )
            
            max_chars = st.number_input(
                "Máximo de caracteres",
                min_value=300,
                max_value=1000,
                value=450,
                help="Comprimento máximo da descrição melhorada"
            )
    
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
                if total_produtos > 100:
                    st.warning(f"⚠️ Arquivo grande detectado: {total_produtos} produtos")
                    st.info("💡 Para evitar timeouts no Streamlit Cloud, recomendamos processar em lotes de 100 produtos")
                    
                    # Opções de processamento
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        processar_lotes = st.button("📦 Processar em Lotes (Recomendado)", type="primary")
                    
                    with col2:
                        processar_tudo = st.button("⚡ Processar Tudo (Risco de Timeout)", type="secondary")
                    
                    if processar_lotes:
                        process_file_in_batches(df, provider, api_key, model, min_ratio, prohibited_phrases, min_chars, max_chars)
                    elif processar_tudo:
                        st.warning("⚠️ Processando todos os produtos de uma vez. Risco de timeout!")
                        process_file(df, provider, api_key, model, min_ratio, prohibited_phrases, min_chars, max_chars)
                else:
                    # Arquivo pequeno, processar normalmente
                    st.success(f"✅ Arquivo pequeno: {total_produtos} produtos")
                    
                    # Mostrar preview dos dados
                    with st.expander("👀 Preview dos Dados"):
                        st.dataframe(df.head(10))
                    
                    # Botão para processar
                    if st.button("🚀 Processar Arquivo", type="primary"):
                        process_file(df, provider, api_key, model, min_ratio, prohibited_phrases, min_chars, max_chars)
                
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

def process_file_in_batches(df: pd.DataFrame, provider: str, api_key: str, model: str, 
                          min_ratio: float, prohibited_phrases: str, min_chars: int, max_chars: int):
    """
    Processa arquivo em lotes para evitar timeouts no Streamlit Cloud.
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
            }
        }
        
        # Criar provedor de IA
        if provider == "openai":
            ai_provider = OpenAIProvider(api_key, model)
        else:
            ai_provider = GeminiProvider(api_key, model)
        
        # Dividir em lotes
        tamanho_lote = 100
        lotes = dividir_em_lotes(df, tamanho_lote)
        total_lotes = len(lotes)
        
        st.header("📦 Processamento em Lotes")
        st.info(f"📊 Arquivo dividido em {total_lotes} lotes de {tamanho_lote} produtos cada")
        
        # Mostrar informações dos lotes
        with st.expander("📋 Informações dos Lotes"):
            for i, lote in enumerate(lotes, 1):
                inicio = lote.index[0] + 1
                fim = lote.index[-1] + 1
                st.write(f"**Lote {i}**: Produtos {inicio} a {fim} ({len(lote)} produtos)")
        
        # Processar cada lote
        resultados = []
        
        for i, lote in enumerate(lotes, 1):
            st.subheader(f"🔄 Processando Lote {i}/{total_lotes}")
            
            # Criar melhorador para este lote
            enhancer = StreamlitProductEnhancer(ai_provider, min_ratio, config, streamlit_logger)
            
            # Área de progresso do lote
            progress_bar = st.progress(0)
            status_text = st.empty()
            enhancer.set_progress_elements(progress_bar, status_text)
            
            # Processar lote
            with st.spinner(f"Processando lote {i}..."):
                lote_resultado = enhancer.process_excel_file_streamlit(lote)
                resultados.append(lote_resultado)
            
            st.success(f"✅ Lote {i} concluído! {len(lote_resultado)} produtos processados")
            
            # Pausa entre lotes para evitar rate limits
            if i < total_lotes:
                st.info("⏳ Aguardando 5 segundos antes do próximo lote...")
                time.sleep(5)
        
        # Combinar resultados
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

def process_file(df: pd.DataFrame, provider: str, api_key: str, model: str, 
                min_ratio: float, prohibited_phrases: str, min_chars: int, max_chars: int):
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
            }
        }
        
        # Criar provedor de IA
        if provider == "openai":
            ai_provider = OpenAIProvider(api_key, model)
        else:
            ai_provider = GeminiProvider(api_key, model)
        
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
            result_df = enhancer.process_excel_file_streamlit(df)
        
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
