#!/usr/bin/env python3
"""
Exemplo de como implementar processamento em lotes para o Streamlit Cloud.
"""

import pandas as pd
import streamlit as st
from typing import List, Tuple

def dividir_em_lotes(df: pd.DataFrame, tamanho_lote: int = 100) -> List[pd.DataFrame]:
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

def processar_lote_streamlit(lote_df: pd.DataFrame, numero_lote: int, total_lotes: int) -> pd.DataFrame:
    """
    Processa um lote específico com feedback visual.
    
    Args:
        lote_df: DataFrame do lote a ser processado
        numero_lote: Número do lote atual (1, 2, 3...)
        total_lotes: Total de lotes
        
    Returns:
        DataFrame processado
    """
    # Mostrar progresso do lote
    st.info(f"🔄 Processando lote {numero_lote}/{total_lotes} ({len(lote_df)} produtos)")
    
    # Criar barra de progresso para o lote
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Simular processamento (substitua pela sua lógica real)
    for index, row in lote_df.iterrows():
        # Atualizar progresso
        progress = (index - lote_df.index[0] + 1) / len(lote_df)
        progress_bar.progress(progress)
        status_text.text(f"Processando produto {index + 1} do lote {numero_lote}")
        
        # Aqui você colocaria a lógica de processamento real
        # Exemplo: chamar o ProductDescriptionEnhancer
        time.sleep(0.1)  # Simular processamento
    
    # Marcar lote como concluído
    st.success(f"✅ Lote {numero_lote} concluído!")
    
    return lote_df

def interface_processamento_lotes():
    """
    Interface Streamlit para processamento em lotes.
    """
    st.header("📦 Processamento em Lotes")
    
    # Upload do arquivo
    uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=['xlsx'])
    
    if uploaded_file is not None:
        # Ler arquivo
        df = pd.read_excel(uploaded_file)
        st.success(f"✅ Arquivo carregado: {len(df)} produtos")
        
        # Configurações do lote
        col1, col2 = st.columns(2)
        
        with col1:
            tamanho_lote = st.number_input(
                "Tamanho do lote",
                min_value=10,
                max_value=200,
                value=100,
                help="Número de produtos por lote (recomendado: 100)"
            )
        
        with col2:
            total_produtos = len(df)
            total_lotes = (total_produtos + tamanho_lote - 1) // tamanho_lote
            st.metric("Total de lotes", total_lotes)
        
        # Mostrar informações dos lotes
        st.subheader("📊 Informações dos Lotes")
        
        lotes = dividir_em_lotes(df, tamanho_lote)
        
        for i, lote in enumerate(lotes, 1):
            inicio = lote.index[0] + 1
            fim = lote.index[-1] + 1
            st.write(f"**Lote {i}**: Produtos {inicio} a {fim} ({len(lote)} produtos)")
        
        # Botão para processar
        if st.button("🚀 Processar Todos os Lotes", type="primary"):
            processar_todos_lotes(df, tamanho_lote)

def processar_todos_lotes(df: pd.DataFrame, tamanho_lote: int):
    """
    Processa todos os lotes sequencialmente.
    """
    lotes = dividir_em_lotes(df, tamanho_lote)
    total_lotes = len(lotes)
    
    st.subheader("🔄 Processamento em Andamento")
    
    resultados = []
    
    for i, lote in enumerate(lotes, 1):
        # Processar lote
        lote_processado = processar_lote_streamlit(lote, i, total_lotes)
        resultados.append(lote_processado)
        
        # Pausa entre lotes para evitar rate limits
        if i < total_lotes:
            st.info("⏳ Aguardando 5 segundos antes do próximo lote...")
            time.sleep(5)
    
    # Combinar resultados
    st.subheader("📋 Combinando Resultados")
    resultado_final = pd.concat(resultados, ignore_index=True)
    
    st.success(f"🎉 Processamento concluído! {len(resultado_final)} produtos processados")
    
    # Botão para download
    csv = resultado_final.to_csv(index=False)
    st.download_button(
        label="📥 Baixar Resultado",
        data=csv,
        file_name="produtos_processados.csv",
        mime="text/csv"
    )

# Exemplo de uso no app.py principal
def exemplo_integracao_app_principal():
    """
    Exemplo de como integrar o processamento em lotes no app.py principal.
    """
    st.header("🎯 Melhorador de Descrições - Processamento em Lotes")
    
    # Verificar se o arquivo é muito grande
    uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=['xlsx'])
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        total_produtos = len(df)
        
        # Se tem mais de 100 produtos, sugerir processamento em lotes
        if total_produtos > 100:
            st.warning(f"⚠️ Arquivo grande detectado: {total_produtos} produtos")
            st.info("💡 Recomendamos processar em lotes de 100 produtos para evitar timeouts")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📦 Processar em Lotes", type="primary"):
                    # Redirecionar para interface de lotes
                    st.session_state['modo_lotes'] = True
                    st.rerun()
            
            with col2:
                if st.button("⚡ Processar Tudo (Risco de Timeout)"):
                    # Processar tudo de uma vez (com risco)
                    st.session_state['modo_lotes'] = False
                    st.rerun()
        else:
            # Arquivo pequeno, processar normalmente
            st.success(f"✅ Arquivo pequeno: {total_produtos} produtos")
            if st.button("🚀 Processar Arquivo", type="primary"):
                # Processamento normal
                pass

if __name__ == "__main__":
    import time
    interface_processamento_lotes()
