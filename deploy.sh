#!/bin/bash
# Script para fazer deploy na AWS Elastic Beanstalk

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Iniciando deploy para AWS Elastic Beanstalk${NC}"

# Verificar se AWS CLI está instalado
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI não encontrado. Instale primeiro:${NC}"
    echo "pip install awscli"
    exit 1
fi

# Verificar se EB CLI está instalado
if ! command -v eb &> /dev/null; then
    echo -e "${RED}❌ EB CLI não encontrado. Instale primeiro:${NC}"
    echo "pip install awsebcli"
    exit 1
fi

# Verificar se está logado na AWS
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}❌ Não está logado na AWS. Execute:${NC}"
    echo "aws configure"
    exit 1
fi

# Nome da aplicação (pode ser alterado)
APP_NAME="compra-agora-script"
ENV_NAME="compra-agora-env"

echo -e "${YELLOW}📋 Configurações:${NC}"
echo "  Aplicação: $APP_NAME"
echo "  Ambiente: $ENV_NAME"

# Verificar se .env existe
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Arquivo .env não encontrado${NC}"
    echo "Criando arquivo .env de exemplo..."
    cp env_example.txt .env
    echo -e "${RED}❌ Configure suas API Keys no arquivo .env antes de continuar${NC}"
    exit 1
fi

# Criar arquivo .ebignore se não existir
if [ ! -f ".ebignore" ]; then
    echo -e "${YELLOW}📝 Criando arquivo .ebignore${NC}"
    cat > .ebignore << EOF
# Arquivos a serem ignorados no deploy
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
*~
EOF
fi

# Verificar se aplicação existe
if ! eb list | grep -q "$APP_NAME"; then
    echo -e "${YELLOW}📱 Criando aplicação Elastic Beanstalk${NC}"
    eb init "$APP_NAME" --platform python-3.11 --region us-east-1
fi

# Verificar se ambiente existe
if ! eb list | grep -q "$ENV_NAME"; then
    echo -e "${YELLOW}🌍 Criando ambiente Elastic Beanstalk${NC}"
    eb create "$ENV_NAME" --instance-type t3.micro
else
    echo -e "${YELLOW}🔄 Fazendo deploy no ambiente existente${NC}"
    eb deploy "$ENV_NAME"
fi

echo -e "${GREEN}✅ Deploy concluído!${NC}"
echo -e "${YELLOW}🌐 URL da aplicação:${NC}"
eb status "$ENV_NAME" | grep "CNAME"

echo -e "${YELLOW}📋 Próximos passos:${NC}"
echo "1. Configure as variáveis de ambiente no console AWS"
echo "2. Acesse a URL da aplicação"
echo "3. Teste a funcionalidade"

echo -e "${GREEN}🎉 Deploy finalizado!${NC}"
