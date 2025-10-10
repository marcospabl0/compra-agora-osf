#!/usr/bin/env python3
"""
Script para testar a correção do erro de progresso.
Cria um arquivo pequeno para testar se o progresso está funcionando corretamente.
"""

import pandas as pd
from datetime import datetime

def criar_arquivo_teste_progresso():
    """Cria um arquivo Excel pequeno para testar o progresso."""
    
    # Lista de produtos simples para teste
    produtos = [
        {
            "Título": "Smartphone Samsung Galaxy A54",
            "Descrição": "Smartphone Samsung",
            "Preço": "R$ 1.299,00",
            "SKU": "SKU0001",
            "Categoria": "Eletrônicos",
            "Marca": "Samsung"
        },
        {
            "Título": "Notebook Dell Inspiron 15",
            "Descrição": "Notebook Dell",
            "Preço": "R$ 2.499,00",
            "SKU": "SKU0002",
            "Categoria": "Eletrônicos",
            "Marca": "Dell"
        },
        {
            "Título": "TV LG 55 Polegadas",
            "Descrição": "TV LG",
            "Preço": "R$ 1.899,00",
            "SKU": "SKU0003",
            "Categoria": "Eletrônicos",
            "Marca": "LG"
        },
        {
            "Título": "Geladeira Brastemp 400L",
            "Descrição": "Geladeira Brastemp",
            "Preço": "R$ 2.199,00",
            "SKU": "SKU0004",
            "Categoria": "Eletrodomésticos",
            "Marca": "Brastemp"
        },
        {
            "Título": "Fogão Consul 4 Bocas",
            "Descrição": "Fogão Consul",
            "Preço": "R$ 899,00",
            "SKU": "SKU0005",
            "Categoria": "Eletrodomésticos",
            "Marca": "Consul"
        }
    ]
    
    # Criar DataFrame
    df = pd.DataFrame(produtos)
    
    # Salvar arquivo
    nome_arquivo = f"teste_progresso_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(nome_arquivo, index=False, engine='openpyxl')
    
    print(f"✅ Arquivo de teste criado: {nome_arquivo}")
    print(f"📊 Total de produtos: {len(df)}")
    print(f"📋 Colunas: {list(df.columns)}")
    
    print("\n🧪 Este arquivo pode ser usado para testar:")
    print("- ✅ Correção do erro de progresso")
    print("- ✅ Processamento em lotes pequenos")
    print("- ✅ Interface Streamlit")
    print("- ✅ Geração de Meta Tags")
    
    return nome_arquivo

if __name__ == "__main__":
    criar_arquivo_teste_progresso()
