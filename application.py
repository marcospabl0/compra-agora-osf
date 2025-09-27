#!/usr/bin/env python3
"""
Arquivo de entrada para AWS Elastic Beanstalk.
Este arquivo é necessário para que o EBS reconheça a aplicação Streamlit.
"""

import os
import subprocess
import sys
from pathlib import Path

def application(environ, start_response):
    """
    WSGI application para AWS Elastic Beanstalk.
    Redireciona para o Streamlit app.
    """
    # Configurar variáveis de ambiente
    os.environ['STREAMLIT_SERVER_PORT'] = '8000'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    # Caminho para o app Streamlit
    app_path = Path(__file__).parent / 'app.py'
    
    # Executar Streamlit
    try:
        # Usar subprocess para executar o Streamlit
        process = subprocess.Popen([
            sys.executable, '-m', 'streamlit', 'run', str(app_path),
            '--server.port=8000',
            '--server.address=0.0.0.0',
            '--server.headless=true',
            '--browser.gatherUsageStats=false'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Retornar resposta básica
        status = '200 OK'
        headers = [('Content-Type', 'text/html')]
        start_response(status, headers)
        
        return [b'<html><body><h1>Streamlit App Running</h1><p>Redirecting to Streamlit...</p></body></html>']
        
    except Exception as e:
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/html')]
        start_response(status, headers)
        
        return [f'<html><body><h1>Error</h1><p>{str(e)}</p></body></html>'.encode()]

if __name__ == '__main__':
    # Para desenvolvimento local
    import streamlit.web.cli as stcli
    import sys
    
    sys.argv = ['streamlit', 'run', 'app.py']
    sys.exit(stcli.main())
