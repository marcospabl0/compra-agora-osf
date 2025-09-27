#!/usr/bin/env python3
"""
Script de exemplo para demonstrar o uso da interface Streamlit.
Cria um arquivo Excel de exemplo com produtos para testar a aplicação.
"""

import pandas as pd
import os
from pathlib import Path

def create_sample_excel():
    """Cria um arquivo Excel de exemplo com produtos para testar a aplicação."""
    
    # Dados de exemplo
    sample_data = {
        'Título': [
            'Smartphone Samsung Galaxy A54 128GB Azul',
            'Whisky Black & White 700mL',
            'Antitranspirante Dove Men+Care 150ml',
            'TV LED Samsung 55" 4K Smart',
            'Notebook Dell Inspiron 15 3000',
            'Refrigerante Coca-Cola 2L',
            'Café Pilão Tradicional 500g',
            'Shampoo Pantene 400ml',
            'Sabonete Dove Original 90g',
            'Chocolate Nestlé Kit Kat 41.5g'
        ],
        'Descrição': [
            'Smartphone Samsung',
            'Whisky escocês',
            'Antitranspirante masculino',
            'TV Samsung',
            'Notebook Dell',
            'Refrigerante Coca-Cola',
            'Café Pilão',
            'Shampoo Pantene',
            'Sabonete Dove',
            'Chocolate Kit Kat'
        ],
        'Preço': [
            'R$ 1.299,00',
            'R$ 89,90',
            'R$ 12,50',
            'R$ 2.499,00',
            'R$ 1.899,00',
            'R$ 6,50',
            'R$ 8,90',
            'R$ 15,90',
            'R$ 3,50',
            'R$ 4,20'
        ],
        'SKU': [
            'SAM-A54-128-AZ',
            'BW-700ML',
            'DOVE-MC-150',
            'SAM-TV-55-4K',
            'DELL-INS-15-3K',
            'COCA-2L',
            'PILAO-500G',
            'PANTENE-400ML',
            'DOVE-SAB-90G',
            'KITKAT-41.5G'
        ],
        'Categoria': [
            'Smartphones',
            'Bebidas',
            'Higiene Pessoal',
            'Eletrônicos',
            'Informática',
            'Bebidas',
            'Alimentos',
            'Higiene Pessoal',
            'Higiene Pessoal',
            'Alimentos'
        ],
        'Marca': [
            'Samsung',
            'Black & White',
            'Dove',
            'Samsung',
            'Dell',
            'Coca-Cola',
            'Pilão',
            'Pantene',
            'Dove',
            'Nestlé'
        ]
    }
    
    # Criar DataFrame
    df = pd.DataFrame(sample_data)
    
    # Salvar arquivo
    output_file = 'exemplo_produtos.xlsx'
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"✅ Arquivo de exemplo criado: {output_file}")
    print(f"📊 Total de produtos: {len(df)}")
    print(f"📁 Localização: {os.path.abspath(output_file)}")
    
    return output_file

def main():
    """Função principal."""
    print("🚀 Criando arquivo de exemplo para testar a interface Streamlit...")
    
    try:
        output_file = create_sample_excel()
        
        print("\n📋 Instruções para usar:")
        print("1. Execute: streamlit run app.py")
        print("2. Faça upload do arquivo:", output_file)
        print("3. Configure sua API Key")
        print("4. Clique em 'Processar Arquivo'")
        print("5. Acompanhe o progresso em tempo real")
        
        print("\n💡 Dicas:")
        print("- Use OpenAI GPT-3.5-turbo para testes (mais rápido e barato)")
        print("- Ajuste a razão mínima para 1.0 para processar todos os produtos")
        print("- Monitore os logs para ver o progresso detalhado")
        
    except Exception as e:
        print(f"❌ Erro ao criar arquivo de exemplo: {str(e)}")

if __name__ == "__main__":
    main()
