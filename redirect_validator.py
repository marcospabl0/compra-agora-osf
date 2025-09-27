#!/usr/bin/env python3
"""
Script para validar redirecionamentos 301 entre URLs antigas e novas.
Lê uma planilha Excel com colunas 'URL Antiga' e 'URL Nova' e verifica se o redirecionamento é 301.
"""

import pandas as pd
import requests
from urllib.parse import urlparse
import time
import logging
from typing import Tuple, Optional

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('redirect_validator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RedirectValidator:
    def __init__(self, timeout: int = 10, max_redirects: int = 5):
        """
        Inicializa o validador de redirecionamentos.
        
        Args:
            timeout: Timeout para requisições HTTP em segundos
            max_redirects: Número máximo de redirecionamentos a seguir
        """
        self.timeout = timeout
        self.max_redirects = max_redirects
        self.session = requests.Session()
        
        # Configurar headers para simular um navegador real
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def validate_redirect(self, old_url: str, new_url: str) -> Tuple[str, str, Optional[str]]:
        """
        Valida se a URL antiga redireciona corretamente para a URL nova com status 301.
        
        Args:
            old_url: URL antiga
            new_url: URL nova esperada
            
        Returns:
            Tuple com (status, resultado, observação)
        """
        try:
            # Normalizar URLs
            old_url = self._normalize_url(old_url)
            new_url = self._normalize_url(new_url)
            
            logger.info(f"Verificando redirecionamento: {old_url} -> {new_url}")
            
            # Fazer requisição sem seguir redirecionamentos automaticamente
            response = self.session.get(
                old_url, 
                timeout=self.timeout, 
                allow_redirects=False,
                verify=False  # Ignorar certificados SSL para testes
            )
            
            # Verificar se há redirecionamento
            if response.status_code in [301, 302, 307, 308]:
                redirect_url = response.headers.get('Location')
                
                if redirect_url:
                    # Normalizar URL de redirecionamento
                    redirect_url = self._normalize_url(redirect_url)
                    
                    # Verificar se redireciona para a URL esperada
                    if redirect_url == new_url:
                        if response.status_code == 301:
                            return "OK", "301", f"Redirecionamento 301 correto para {new_url}"
                        else:
                            return "NOK", f"{response.status_code}", f"Redirecionamento {response.status_code} (esperado 301) para {new_url}"
                    else:
                        return "NOK", f"{response.status_code}", f"Redirecionamento para {redirect_url} (esperado {new_url})"
                else:
                    return "NOK", f"{response.status_code}", "Sem header Location"
            else:
                return "NOK", f"{response.status_code}", f"Sem redirecionamento (status {response.status_code})"
                
        except requests.exceptions.Timeout:
            return "NOK", "TIMEOUT", "Timeout na requisição"
        except requests.exceptions.ConnectionError:
            return "NOK", "CONNECTION_ERROR", "Erro de conexão"
        except requests.exceptions.RequestException as e:
            return "NOK", "REQUEST_ERROR", f"Erro na requisição: {str(e)}"
        except Exception as e:
            return "NOK", "UNKNOWN_ERROR", f"Erro desconhecido: {str(e)}"

    def _normalize_url(self, url: str) -> str:
        """
        Normaliza uma URL removendo fragmentos e normalizando a estrutura.
        
        Args:
            url: URL para normalizar
            
        Returns:
            URL normalizada
        """
        if not url:
            return ""
            
        # Adicionar protocolo se não existir
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        # Parse da URL
        parsed = urlparse(url)
        
        # Remover fragmentos (#) e normalizar
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        
        # Adicionar query string se existir
        if parsed.query:
            normalized += f"?{parsed.query}"
            
        return normalized

    def process_excel_file(self, input_file: str, output_file: str = None) -> None:
        """
        Processa um arquivo Excel com URLs e valida os redirecionamentos.
        
        Args:
            input_file: Caminho do arquivo Excel de entrada
            output_file: Caminho do arquivo Excel de saída (opcional)
        """
        try:
            # Ler planilha
            logger.info(f"Lendo arquivo: {input_file}")
            df = pd.read_excel(input_file)
            
            # Verificar colunas necessárias
            required_columns = ['URL Antiga', 'URL Nova']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"Colunas necessárias não encontradas: {missing_columns}")
            
            # Adicionar colunas de resultado se não existirem
            if 'Status' not in df.columns:
                df['Status'] = ''
            if 'Código HTTP' not in df.columns:
                df['Código HTTP'] = ''
            if 'Observação' not in df.columns:
                df['Observação'] = ''
            
            # Processar cada linha
            total_rows = len(df)
            logger.info(f"Processando {total_rows} URLs...")
            
            for index, row in df.iterrows():
                old_url = str(row['URL Antiga']).strip()
                new_url = str(row['URL Nova']).strip()
                
                # Pular linhas vazias
                if not old_url or not new_url or old_url == 'nan' or new_url == 'nan':
                    df.at[index, 'Status'] = 'SKIP'
                    df.at[index, 'Código HTTP'] = ''
                    df.at[index, 'Observação'] = 'URL vazia'
                    continue
                
                # Validar redirecionamento
                status, http_code, observation = self.validate_redirect(old_url, new_url)
                
                # Atualizar DataFrame
                df.at[index, 'Status'] = status
                df.at[index, 'Código HTTP'] = http_code
                df.at[index, 'Observação'] = observation
                
                # Log do progresso
                logger.info(f"Linha {index + 1}/{total_rows}: {status} - {old_url} -> {new_url}")
                
                # Pequena pausa para não sobrecarregar servidores
                time.sleep(0.5)
            
            # Salvar resultado
            output_file = output_file or input_file.replace('.xlsx', '_validado.xlsx').replace('.xls', '_validado.xlsx')
            df.to_excel(output_file, index=False)
            
            # Estatísticas
            ok_count = len(df[df['Status'] == 'OK'])
            nok_count = len(df[df['Status'] == 'NOK'])
            skip_count = len(df[df['Status'] == 'SKIP'])
            
            logger.info(f"Processamento concluído!")
            logger.info(f"OK: {ok_count}, NOK: {nok_count}, SKIP: {skip_count}")
            logger.info(f"Arquivo salvo: {output_file}")
            
        except Exception as e:
            logger.error(f"Erro ao processar arquivo: {str(e)}")
            raise

def main():
    """Função principal do script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validador de redirecionamentos 301')
    parser.add_argument('input_file', help='Arquivo Excel de entrada')
    parser.add_argument('-o', '--output', help='Arquivo Excel de saída (opcional)')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Timeout em segundos (padrão: 10)')
    parser.add_argument('-r', '--max-redirects', type=int, default=5, help='Máximo de redirecionamentos (padrão: 5)')
    
    args = parser.parse_args()
    
    # Criar validador
    validator = RedirectValidator(timeout=args.timeout, max_redirects=args.max_redirects)
    
    # Processar arquivo
    validator.process_excel_file(args.input_file, args.output)

if __name__ == "__main__":
    main() 