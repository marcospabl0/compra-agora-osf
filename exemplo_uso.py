#!/usr/bin/env python3
"""
Exemplo de uso do validador de redirecionamentos.
Este script demonstra como usar o RedirectValidator programaticamente.
"""

import pandas as pd
from redirect_validator import RedirectValidator

def criar_planilha_exemplo():
    """Cria uma planilha de exemplo para teste."""
    
    # Dados de exemplo
    dados = {
        'URL Antiga': [
            'https://httpstat.us/301',
            'https://httpstat.us/302', 
            'https://httpstat.us/404',
            'https://exemplo.com/pagina-antiga',
            'https://site.com/old-page'
        ],
        'URL Nova': [
            'https://httpstat.us/200',
            'https://httpstat.us/200',
            'https://httpstat.us/200',
            'https://exemplo.com/pagina-nova',
            'https://site.com/new-page'
        ]
    }
    
    df = pd.DataFrame(dados)
    df.to_excel('exemplo_urls.xlsx', index=False)
    print("Planilha de exemplo criada: exemplo_urls.xlsx")

def exemplo_uso_programatico():
    """Demonstra como usar o validador programaticamente."""
    
    # Criar validador
    validator = RedirectValidator(timeout=10)
    
    # Exemplo de validação individual
    print("=== Validação Individual ===")
    old_url = "https://httpstat.us/301"
    new_url = "https://httpstat.us/200"
    
    status, http_code, observation = validator.validate_redirect(old_url, new_url)
    print(f"URL Antiga: {old_url}")
    print(f"URL Nova: {new_url}")
    print(f"Status: {status}")
    print(f"Código HTTP: {http_code}")
    print(f"Observação: {observation}")
    print()

def exemplo_processamento_arquivo():
    """Demonstra como processar um arquivo Excel."""
    
    print("=== Processamento de Arquivo ===")
    
    # Criar validador
    validator = RedirectValidator(timeout=10)
    
    try:
        # Processar arquivo
        validator.process_excel_file('exemplo_urls.xlsx', 'resultado_validacao.xlsx')
        print("Processamento concluído! Verifique o arquivo 'resultado_validacao.xlsx'")
        
    except FileNotFoundError:
        print("Arquivo 'exemplo_urls.xlsx' não encontrado. Execute primeiro criar_planilha_exemplo()")
    except Exception as e:
        print(f"Erro durante o processamento: {e}")

def exemplo_validacao_multipla():
    """Demonstra validação de múltiplas URLs."""
    
    print("=== Validação Múltipla ===")
    
    # Lista de URLs para testar
    urls_para_testar = [
        ("https://httpstat.us/301", "https://httpstat.us/200"),
        ("https://httpstat.us/302", "https://httpstat.us/200"),
        ("https://httpstat.us/404", "https://httpstat.us/200"),
    ]
    
    validator = RedirectValidator(timeout=10)
    
    resultados = []
    
    for old_url, new_url in urls_para_testar:
        status, http_code, observation = validator.validate_redirect(old_url, new_url)
        resultados.append({
            'URL Antiga': old_url,
            'URL Nova': new_url,
            'Status': status,
            'Código HTTP': http_code,
            'Observação': observation
        })
        print(f"{old_url} -> {new_url}: {status} ({http_code})")
    
    # Salvar resultados
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_excel('resultados_validacao.xlsx', index=False)
    print("\nResultados salvos em 'resultados_validacao.xlsx'")

if __name__ == "__main__":
    print("=== Exemplos de Uso do Validador de Redirecionamentos ===\n")
    
    # Criar planilha de exemplo
    print("1. Criando planilha de exemplo...")
    criar_planilha_exemplo()
    print()
    
    # Exemplo de validação individual
    print("2. Exemplo de validação individual:")
    exemplo_uso_programatico()
    
    # Exemplo de validação múltipla
    print("3. Exemplo de validação múltipla:")
    exemplo_validacao_multipla()
    print()
    
    # Exemplo de processamento de arquivo
    print("4. Exemplo de processamento de arquivo:")
    exemplo_processamento_arquivo()
    print()
    
    print("=== Todos os exemplos concluídos! ===")
    print("Arquivos gerados:")
    print("- exemplo_urls.xlsx (planilha de exemplo)")
    print("- resultado_validacao.xlsx (resultado do processamento)")
    print("- resultados_validacao.xlsx (validação múltipla)")
    print("- redirect_validator.log (logs do processo)") 