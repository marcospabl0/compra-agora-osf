#!/usr/bin/env python3
"""
Script para criar um arquivo de exemplo com 1000 produtos para testar
o processamento em lotes otimizado.
"""

import pandas as pd
import random
from datetime import datetime

def criar_arquivo_exemplo_grande():
    """Cria um arquivo Excel com 1000 produtos para teste."""
    
    # Listas de dados para gerar produtos variados
    marcas = [
        "Samsung", "Apple", "LG", "Sony", "Panasonic", "Philips", "Whirlpool", 
        "Electrolux", "Brastemp", "Consul", "Nestlé", "Coca-Cola", "Pepsi",
        "Unilever", "P&G", "Johnson & Johnson", "Nike", "Adidas", "Puma",
        "Nike", "Adidas", "Puma", "Reebok", "New Balance", "Converse"
    ]
    
    categorias = [
        "Eletrônicos", "Eletrodomésticos", "Casa e Jardim", "Esportes", 
        "Beleza e Saúde", "Alimentação", "Roupas", "Calçados", "Livros",
        "Brinquedos", "Automotivo", "Ferramentas", "Móveis", "Decoração"
    ]
    
    produtos_base = [
        "Smartphone", "Notebook", "TV", "Geladeira", "Fogão", "Micro-ondas",
        "Liquidificador", "Aspirador", "Ventilador", "Ar Condicionado",
        "Cafeteira", "Sanduicheira", "Panela Elétrica", "Ferro de Passar",
        "Secador de Cabelo", "Escova de Dentes", "Sabonete", "Shampoo",
        "Condicionador", "Creme Facial", "Protetor Solar", "Desodorante",
        "Antitranspirante", "Perfume", "Colônia", "Loção Pós-Barba",
        "Tênis", "Sapato", "Sandália", "Chinelo", "Camiseta", "Calça",
        "Short", "Vestido", "Blusa", "Jaqueta", "Casaco", "Moletom",
        "Livro", "Revista", "Caderno", "Caneta", "Lápis", "Borracha",
        "Brinquedo", "Boneca", "Carrinho", "Bola", "Quebra-cabeça",
        "Jogo de Tabuleiro", "Videogame", "Console", "Controle",
        "Ferramenta", "Martelo", "Chave de Fenda", "Alicate", "Furadeira",
        "Parafuso", "Porca", "Arruela", "Prego", "Tinta", "Pincel",
        "Mesa", "Cadeira", "Sofá", "Cama", "Guarda-roupa", "Estante",
        "Quadro", "Vaso", "Luminária", "Cortina", "Tapete", "Almofada"
    ]
    
    # Gerar 1000 produtos
    produtos = []
    
    for i in range(1000):
        produto_base = random.choice(produtos_base)
        marca = random.choice(marcas)
        categoria = random.choice(categorias)
        
        # Gerar título variado
        if random.random() < 0.3:  # 30% chance de ter especificações técnicas
            especificacoes = [
                f"{random.randint(1, 10)}GB", f"{random.randint(100, 2000)}mL",
                f"{random.randint(20, 80)}cm", f"{random.randint(1, 50)}kg",
                f"{random.randint(1, 100)}W", f"{random.randint(1, 12)}V",
                "Azul", "Vermelho", "Verde", "Preto", "Branco", "Cinza",
                "P", "M", "G", "GG", "XG", "PP"
            ]
            espec = random.choice(especificacoes)
            titulo = f"{produto_base} {marca} {espec}"
        else:
            titulo = f"{produto_base} {marca}"
        
        # Gerar descrição variada (algumas curtas, outras médias)
        if random.random() < 0.4:  # 40% chance de descrição curta
            descricao = produto_base
        elif random.random() < 0.7:  # 30% chance de descrição média
            descricao = f"{produto_base} {marca} com qualidade superior"
        else:  # 30% chance de descrição mais longa
            descricao = f"{produto_base} {marca} oferece excelente qualidade e durabilidade. Produto desenvolvido com tecnologia avançada para atender suas necessidades com máxima eficiência e confiabilidade."
        
        # Gerar preço
        preco = round(random.uniform(10, 2000), 2)
        
        # Gerar SKU
        sku = f"SKU{1000 + i:04d}"
        
        produtos.append({
            "Título": titulo,
            "Descrição": descricao,
            "Preço": f"R$ {preco:.2f}",
            "SKU": sku,
            "Categoria": categoria,
            "Marca": marca
        })
    
    # Criar DataFrame
    df = pd.DataFrame(produtos)
    
    # Salvar arquivo
    nome_arquivo = f"exemplo_1000_produtos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(nome_arquivo, index=False, engine='openpyxl')
    
    print(f"✅ Arquivo criado: {nome_arquivo}")
    print(f"📊 Total de produtos: {len(df)}")
    print(f"📋 Colunas: {list(df.columns)}")
    
    # Mostrar estatísticas
    print("\n📈 Estatísticas:")
    print(f"- Produtos com descrição curta: {len(df[df['Descrição'].str.len() < 20])}")
    print(f"- Produtos com descrição média: {len(df[(df['Descrição'].str.len() >= 20) & (df['Descrição'].str.len() < 50)])}")
    print(f"- Produtos com descrição longa: {len(df[df['Descrição'].str.len() >= 50])}")
    print(f"- Categorias únicas: {df['Categoria'].nunique()}")
    print(f"- Marcas únicas: {df['Marca'].nunique()}")
    
    return nome_arquivo

if __name__ == "__main__":
    criar_arquivo_exemplo_grande()
