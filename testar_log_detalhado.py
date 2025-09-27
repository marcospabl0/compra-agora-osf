#!/usr/bin/env python3
"""
Script para testar o log detalhado com descrições antes e depois.
"""

import pandas as pd
from product_description_enhancer import ProductDescriptionEnhancer, OpenAIProvider
from dotenv import load_dotenv
import os
import logging

def testar_log_detalhado():
    """Testa o log detalhado com alguns produtos."""
    
    # Configurar logging para mostrar no console
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    
    # Carregar variáveis de ambiente
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OPENAI_API_KEY não encontrada no arquivo .env")
        return
    
    # Criar provedor OpenAI
    ai_provider = OpenAIProvider(api_key, model="gpt-3.5-turbo")
    
    # Criar melhorador
    enhancer = ProductDescriptionEnhancer(ai_provider, min_description_ratio=1.5)
    
    # Produtos de teste
    produtos_teste = [
        {
            'title': 'Desodorante Suave Antitranspirante Roll-On Hidratação Vera 50mL',
            'description': 'Desodorante Suave Antitranspirante Roll-On Hidratação Vera 50mL',
            'price': 'R$ 15,90',
            'sku': 'DOVE-VERA-50ML',
            'category': 'Higiene Pessoal',
            'brand': 'Dove'
        },
        {
            'title': 'Fita Strip Mãe Terra',
            'description': 'Fita Strip Mãe Terra',
            'price': 'R$ 8,50',
            'sku': 'MAE-TERRA-STRIP',
            'category': 'Decoração',
            'brand': 'Mãe Terra'
        },
        {
            'title': 'Hangtab',
            'description': 'Hangtab Mãe Terra',
            'price': 'R$ 5,90',
            'sku': 'MAE-TERRA-HANGTAB',
            'category': 'Decoração',
            'brand': 'Mãe Terra'
        }
    ]
    
    print("🧪 TESTE DO LOG DETALHADO")
    print("=" * 60)
    
    for i, produto_data in enumerate(produtos_teste, 1):
        print(f"\n📦 PRODUTO {i}:")
        print(f"Título: {produto_data['title']}")
        print(f"Descrição atual: {produto_data['description']}")
        
        # Criar objeto ProductInfo
        from product_description_enhancer import ProductInfo
        product = ProductInfo(
            title=produto_data['title'],
            description=produto_data['description'],
            price=produto_data['price'],
            sku=produto_data['sku'],
            category=produto_data['category'],
            brand=produto_data['brand']
        )
        
        # Verificar se deve melhorar
        should_enhance, motivo = enhancer.should_enhance_description(product.title, product.description)
        
        if should_enhance:
            print(f"🔴 Status: SERÁ MELHORADO (Motivo: {motivo})")
            
            # Perguntar se quer testar a melhoria
            resposta = input(f"🤔 Deseja testar a melhoria para este produto? (s/n): ").lower().strip()
            
            if resposta in ['s', 'sim', 'y', 'yes']:
                print("🔄 Gerando nova descrição...")
                try:
                    # Simular o log detalhado
                    print(f"  📝 Descrição ATUAL: {product.description}")
                    
                    nova_descricao = ai_provider.enhance_description(product)
                    
                    print(f"  ✨ Descrição MELHORADA: {nova_descricao}")
                    print(f"  📊 Tamanho: {len(product.description)} → {len(nova_descricao)} caracteres")
                    
                except Exception as e:
                    print(f"❌ Erro: {str(e)}")
            else:
                print("⏸️ Teste pulado.")
        else:
            print(f"🟢 Status: NÃO SERÁ MELHORADO (Motivo: {motivo})")
            print(f"  ✅ MANTIDO: {product.title[:50]}... (Motivo: {motivo})")
        
        print("-" * 60)

if __name__ == "__main__":
    testar_log_detalhado() 