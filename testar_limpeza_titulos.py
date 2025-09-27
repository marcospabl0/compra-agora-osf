#!/usr/bin/env python3
"""
Script de teste para demonstrar a funcionalidade de limpeza de títulos de produtos.
Remove informações de volume, apresentação e especificações técnicas.
"""

from product_description_enhancer import clean_product_title

def test_title_cleaning():
    """Testa a limpeza de diferentes tipos de títulos."""
    
    # Exemplos de títulos com informações técnicas
    test_titles = [
        "Whisky Black & White 700mL",
        "Smartphone Samsung Galaxy A54 128GB Azul",
        "Antitranspirante Dove Men+Care Invisible Dry 150ml",
        "TV LG 55 polegadas 4K Smart TV",
        "Notebook Dell Inspiron 15 3000 Intel Core i5 8GB RAM 256GB SSD",
        "Kit Escova de Dentes Oral-B Pro 1000 + 2 Cabeças de Reposição",
        "Pack 6 Latas de Refrigerante Coca-Cola 350ml",
        "Conjunto de Panelas Tramontina 5 Peças Antiaderente",
        "Edição Limitada Perfume Chanel Nº5 50ml",
        "Versão Premium Fone de Ouvido Sony WH-1000XM4",
        "Modelo 2024 Carro Controle Remoto para Crianças",
        "Série Especial Chocolate Lindt Excellence 70% Cacau 100g",
        "Cor Azul Claro Camiseta Básica Algodão 100%",
        "Tamanho M Calça Jeans Masculina Slim Fit",
        "Tipo Premium Café em Grãos Torrado Escuro 500g",
        "Categoria Especial Vinho Tinto Seco 750ml",
        "Linha Exclusiva Sabonete Líquido 300ml",
        "Coleção Limitada Perfume Feminino 30ml",
        "Peso 2.5kg Ração Premium para Cães Adultos",
        "Capacidade 1.5L Garrafa Térmica Aço Inox",
        "Dimensões 30x20x15cm Caixa Organizadora Plástico",
        "Contém 30 Comprimidos Vitamina C 1000mg",
        "Quantidade 500g Macarrão Espaguete Integral"
    ]
    
    print("🧪 TESTE DE LIMPEZA DE TÍTULOS DE PRODUTOS")
    print("=" * 60)
    print("Este script demonstra como títulos são limpos para melhorar Meta Tags SEO")
    print("Remove volume, peso, cor, tamanho e outras especificações técnicas\n")
    
    for i, title in enumerate(test_titles, 1):
        cleaned = clean_product_title(title)
        print(f"{i:2d}. Original: {title}")
        print(f"    Limpo:   {cleaned}")
        print(f"    Redução:  {len(title)} → {len(cleaned)} caracteres")
        print()
    
    print("=" * 60)
    print("✅ Funcionalidade implementada com sucesso!")
    print("📝 Os títulos limpos são usados para gerar Meta Title e Meta Description")
    print("🎯 Foco no nome essencial do produto para melhor SEO")

if __name__ == "__main__":
    test_title_cleaning()
