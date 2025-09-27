# 🚀 Deploy na AWS Elastic Beanstalk

Este guia explica como publicar o projeto "Compra Agora Script" na AWS usando Elastic Beanstalk.

## 📋 Pré-requisitos

### 1. Conta AWS

- Conta AWS ativa
- Acesso ao console AWS
- Permissões para Elastic Beanstalk

### 2. Ferramentas Necessárias

```bash
# Instalar AWS CLI
pip install awscli

# Instalar EB CLI
pip install awsebcli

# Configurar AWS CLI
aws configure
```

### 3. Configuração AWS

```bash
# Configurar credenciais
aws configure
# AWS Access Key ID: [sua-chave]
# AWS Secret Access Key: [sua-chave-secreta]
# Default region name: us-east-1
# Default output format: json
```

## 🔧 Configuração do Projeto

### 1. Arquivos Criados para Deploy

#### `application.py`

- Ponto de entrada para Elastic Beanstalk
- Configura Streamlit para produção
- Trata requisições WSGI

#### `.ebextensions/`

- **01_python.config**: Configurações básicas do Python
- **02_dependencies.config**: Instalação de dependências
- **03_streamlit.config**: Configurações específicas do Streamlit

#### `requirements-prod.txt`

- Dependências para produção
- Inclui gunicorn e boto3

#### Scripts de Deploy

- **deploy.sh**: Script bash para Linux/Mac
- **deploy.py**: Script Python para Windows

### 2. Configuração de Variáveis de Ambiente

#### No Console AWS:

1. Acesse Elastic Beanstalk
2. Selecione sua aplicação
3. Vá em "Configuration" → "Software"
4. Adicione as variáveis:

```
OPENAI_API_KEY = sk-sua-chave-openai
GEMINI_API_KEY = sua-chave-gemini
STREAMLIT_SERVER_PORT = 8000
STREAMLIT_SERVER_ADDRESS = 0.0.0.0
STREAMLIT_SERVER_HEADLESS = true
```

## 🚀 Processo de Deploy

### Método 1: Script Automático (Recomendado)

#### Linux/Mac:

```bash
# Tornar executável
chmod +x deploy.sh

# Executar deploy
./deploy.sh
```

#### Windows:

```bash
# Executar script Python
python deploy.py
```

### Método 2: Deploy Manual

#### 1. Inicializar Aplicação

```bash
eb init compra-agora-script --platform python-3.11 --region us-east-1
```

#### 2. Criar Ambiente

```bash
eb create compra-agora-env --instance-type t3.micro
```

#### 3. Deploy

```bash
eb deploy compra-agora-env
```

#### 4. Verificar Status

```bash
eb status compra-agora-env
```

## 🔍 Verificação e Testes

### 1. Verificar Deploy

```bash
# Status da aplicação
eb status

# Logs da aplicação
eb logs

# Abrir aplicação no navegador
eb open
```

### 2. Testes Funcionais

1. Acesse a URL da aplicação
2. Verifique se a interface carrega
3. Teste upload de arquivo
4. Verifique processamento
5. Teste download de resultados

## 🛠️ Configurações Avançadas

### 1. Instância Personalizada

```bash
# Criar com instância específica
eb create compra-agora-env --instance-type t3.small
```

### 2. Configurações de Ambiente

```bash
# Configurar variáveis via CLI
eb setenv OPENAI_API_KEY=sk-sua-chave
eb setenv GEMINI_API_KEY=sua-chave-gemini
```

### 3. Monitoramento

```bash
# Ver logs em tempo real
eb logs --follow

# Verificar saúde da aplicação
eb health
```

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. Erro de Dependências

```bash
# Verificar logs
eb logs

# Reinstalar dependências
eb deploy --force
```

#### 2. Erro de Variáveis de Ambiente

```bash
# Verificar configurações
eb config

# Reconfigurar variáveis
eb setenv VARIAVEL=valor
```

#### 3. Erro de Porta

```bash
# Verificar configurações de porta
eb config

# Ajustar configurações do Streamlit
eb setenv STREAMLIT_SERVER_PORT=8000
```

#### 4. Erro de Memória

```bash
# Aumentar tamanho da instância
eb scale --instance-type t3.small
```

### Logs Importantes

#### Logs da Aplicação

```bash
eb logs --all
```

#### Logs do Sistema

```bash
eb logs --all --all
```

## 💰 Custos e Otimização

### 1. Instâncias Recomendadas

- **Desenvolvimento**: t3.micro (gratuito)
- **Produção**: t3.small ou t3.medium
- **Alto tráfego**: t3.large ou superior

### 2. Otimizações de Custo

```bash
# Configurar auto-scaling
eb config

# Configurar load balancer
eb create --loadbalancer-type application
```

### 3. Monitoramento de Custos

- Use AWS Cost Explorer
- Configure alertas de billing
- Monitore uso de recursos

## 🔒 Segurança

### 1. Variáveis de Ambiente

- Nunca commite API Keys
- Use variáveis de ambiente do EBS
- Rotacione chaves regularmente

### 2. Acesso à Aplicação

```bash
# Configurar HTTPS
eb config

# Configurar autenticação
eb setenv STREAMLIT_AUTHENTICATION=true
```

### 3. Backup

```bash
# Backup da aplicação
eb create --source compra-agora-env backup-env
```

## 📊 Monitoramento e Métricas

### 1. CloudWatch

- Métricas de CPU e memória
- Logs centralizados
- Alertas automáticos

### 2. Health Checks

```bash
# Verificar saúde
eb health

# Configurar health checks
eb config
```

### 3. Performance

- Monitorar tempo de resposta
- Acompanhar uso de recursos
- Otimizar conforme necessário

## 🎯 Próximos Passos

### 1. Produção

- Configurar domínio personalizado
- Implementar HTTPS
- Configurar CDN

### 2. Escalabilidade

- Configurar auto-scaling
- Implementar load balancer
- Otimizar performance

### 3. Monitoramento

- Configurar alertas
- Implementar logging
- Monitorar métricas

## 📞 Suporte

### Recursos AWS

- [Documentação Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/)
- [AWS Support](https://aws.amazon.com/support/)

### Troubleshooting

- Verifique logs da aplicação
- Consulte documentação AWS
- Use AWS Support se necessário

## 🎉 Conclusão

Com este guia, você pode:

- ✅ Fazer deploy automático na AWS
- ✅ Configurar ambiente de produção
- ✅ Monitorar e otimizar a aplicação
- ✅ Resolver problemas comuns
- ✅ Escalar conforme necessário

A aplicação estará disponível 24/7 na AWS com alta disponibilidade e escalabilidade automática!
