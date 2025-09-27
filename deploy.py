#!/usr/bin/env python3
"""
Script Python para fazer deploy na AWS Elastic Beanstalk.
Alternativa ao script bash para usuários Windows.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Executa um comando e trata erros."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} concluído")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}: {e.stderr}")
        return None

def check_dependencies():
    """Verifica se as dependências estão instaladas."""
    print("🔍 Verificando dependências...")
    
    # Verificar AWS CLI
    if not shutil.which('aws'):
        print("❌ AWS CLI não encontrado. Instale primeiro:")
        print("pip install awscli")
        return False
    
    # Verificar EB CLI
    if not shutil.which('eb'):
        print("❌ EB CLI não encontrado. Instale primeiro:")
        print("pip install awsebcli")
        return False
    
    print("✅ Dependências verificadas")
    return True

def check_aws_login():
    """Verifica se está logado na AWS."""
    print("🔍 Verificando login AWS...")
    result = run_command("aws sts get-caller-identity", "Verificação de login")
    if result is None:
        print("❌ Não está logado na AWS. Execute:")
        print("aws configure")
        return False
    
    print("✅ Login AWS verificado")
    return True

def create_ebignore():
    """Cria arquivo .ebignore se não existir."""
    ebignore_path = Path('.ebignore')
    if not ebignore_path.exists():
        print("📝 Criando arquivo .ebignore...")
        ebignore_content = """# Arquivos a serem ignorados no deploy
.env
*.log
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git/
.mypy_cache/
.pytest_cache/
.hypothesis/
.DS_Store
.vscode/
.idea/
*.swp
*.swo
*~"""
        
        with open(ebignore_path, 'w') as f:
            f.write(ebignore_content)
        print("✅ Arquivo .ebignore criado")

def check_env_file():
    """Verifica se arquivo .env existe."""
    env_path = Path('.env')
    if not env_path.exists():
        print("⚠️  Arquivo .env não encontrado")
        example_path = Path('env_example.txt')
        if example_path.exists():
            print("📝 Copiando arquivo de exemplo...")
            shutil.copy(example_path, env_path)
            print("✅ Arquivo .env criado")
        else:
            print("❌ Arquivo env_example.txt não encontrado")
            return False
        
        print("❌ Configure suas API Keys no arquivo .env antes de continuar")
        return False
    
    print("✅ Arquivo .env encontrado")
    return True

def deploy_to_eb():
    """Faz o deploy para Elastic Beanstalk."""
    app_name = "compra-agora-script"
    env_name = "compra-agora-env"
    
    print(f"📋 Configurações:")
    print(f"  Aplicação: {app_name}")
    print(f"  Ambiente: {env_name}")
    
    # Verificar se aplicação existe
    result = run_command("eb list", "Listando aplicações")
    if result and app_name not in result:
        print(f"📱 Criando aplicação {app_name}...")
        init_cmd = f"eb init {app_name} --platform python-3.11 --region us-east-1"
        run_command(init_cmd, "Inicializando aplicação")
    
    # Verificar se ambiente existe
    result = run_command("eb list", "Listando ambientes")
    if result and env_name not in result:
        print(f"🌍 Criando ambiente {env_name}...")
        create_cmd = f"eb create {env_name} --instance-type t3.micro"
        run_command(create_cmd, "Criando ambiente")
    else:
        print(f"🔄 Fazendo deploy no ambiente {env_name}...")
        deploy_cmd = f"eb deploy {env_name}"
        run_command(deploy_cmd, "Deploy no ambiente")
    
    # Obter URL da aplicação
    print("🌐 Obtendo URL da aplicação...")
    result = run_command(f"eb status {env_name}", "Status do ambiente")
    if result:
        lines = result.split('\n')
        for line in lines:
            if 'CNAME' in line:
                print(f"🌐 URL: {line.strip()}")
                break

def main():
    """Função principal."""
    print("🚀 Iniciando deploy para AWS Elastic Beanstalk")
    print("=" * 50)
    
    # Verificações
    if not check_dependencies():
        return
    
    if not check_aws_login():
        return
    
    if not check_env_file():
        return
    
    # Preparação
    create_ebignore()
    
    # Deploy
    deploy_to_eb()
    
    print("=" * 50)
    print("✅ Deploy concluído!")
    print("📋 Próximos passos:")
    print("1. Configure as variáveis de ambiente no console AWS")
    print("2. Acesse a URL da aplicação")
    print("3. Teste a funcionalidade")
    print("🎉 Deploy finalizado!")

if __name__ == "__main__":
    main()
