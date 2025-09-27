# Scripts de Automação para E-commerce

Este repositório contém scripts Python para automação de tarefas comuns em e-commerce:

## 📁 Scripts Disponíveis

### 1. Validador de Redirecionamentos 301

Valida se URLs antigas redirecionam corretamente para URLs novas com status HTTP 301.

### 2. Melhorador de Descrições de Produtos com SEO

Melhora descrições de produtos usando IA (OpenAI/Gemini) quando são muito curtas e **gera Meta Title e Meta Description otimizados para SEO**.

### 3. 🆕 Interface Streamlit (app.py)

**Interface web interativa** para o melhorador de descrições com:

- Upload de arquivos Excel
- Configuração visual de parâmetros
- Monitoramento em tempo real
- Logs detalhados
- Download de resultados

### 4. 🚀 Deploy na AWS Elastic Beanstalk

**Deploy automático na nuvem** com:

- Scripts de deploy automatizados
- Configurações de produção
- Escalabilidade automática
- Monitoramento integrado

## 🚀 Funcionalidades

### Validador de Redirecionamentos 301

- ✅ Lê planilhas Excel com colunas "URL Antiga" e "URL Nova"
- ✅ Verifica se o redirecionamento é 301 (permanente)
- ✅ Marca resultados como "OK" ou "NOK" na planilha
- ✅ Gera logs detalhados do processo
- ✅ Suporta diferentes formatos de URL
- ✅ Tratamento de erros robusto

### Melhorador de Descrições de Produtos com SEO

- ✅ Processa catálogos completos de produtos
- ✅ Identifica descrições muito curtas (razão título/descrição < 1.5)
- ✅ Usa OpenAI GPT ou Google Gemini para melhorar descrições
- ✅ Cria descrições detalhadas e persuasivas
- ✅ **Gera Meta Title otimizado para SEO (máx. 60 caracteres)**
- ✅ **Gera Meta Description otimizada para SEO (máx. 160 caracteres)**
- ✅ **🆕 Limpa automaticamente títulos removendo volume, peso, cor, tamanho e especificações técnicas**
- ✅ Mantém informações originais (preço, SKU, categoria, marca)
- ✅ Gera estatísticas de processamento
- ✅ Suporta mapeamento personalizado de colunas
- ✅ **Aplica boas práticas de SEO para e-commerce**

## 🆕 Novas Funcionalidades de SEO

### 🧹 Limpeza Automática de Títulos

- **Remove automaticamente informações técnicas desnecessárias** para SEO
- **Volumes e medidas**: 700mL, 500g, 55 polegadas, etc.
- **Apresentações**: Pack, Kit, Conjunto, Set, etc.
- **Especificações técnicas**: Edição Limitada, Versão Premium, Modelo 2024, etc.
- **Cores e tamanhos**: Azul, M, GG, etc. (quando não essenciais)
- **Dimensões e pesos**: 30x20x15cm, 2.5kg, etc.
- **Quantidades**: Contém 30 comprimidos, 6 latas, etc.
- **Resultado**: Títulos focados no produto em si, otimizados para SEO

**Exemplos de limpeza:**

- `"Whisky Black & White 700mL"` → `"Whisky Black & White"`
- `"Smartphone Samsung Galaxy A54 128GB Azul"` → `"Smartphone Samsung Galaxy A54"`
- `"Pack 6 Latas de Refrigerante Coca-Cola 350ml"` → `"Refrigerante Coca-Cola"`

### Meta Title (Título SEO)

- **Otimizado para mecanismos de busca seguindo as regras do Compra Agora**
- **Entre 50 e 60 caracteres** (padrão Google)
- **Formato**: "Nome Produto | Marca - Compra Agora"
- **Palavra-chave principal no início** sempre que possível
- **Inclui nome da marca no final**
- **Sufixo "- Compra Agora"** (consome 15 caracteres)
- **Atrativo para cliques**
- **🆕 Títulos automaticamente limpos** (sem volume, peso, cor, tamanho ou especificações técnicas)

### Meta Description

- **Descrição para resultados de busca seguindo as regras do Compra Agora**
- **Entre 140 e 160 caracteres** (padrão Google)
- **Palavra-chave principal de forma natural**
- **Explicação clara do que o usuário encontra na página**
- **Gatilhos de ação** ("Compre agora", "Descubra", "Veja modelos exclusivos")
- **Benefícios e diferenciais** destacados
- **Sem duplicação** entre páginas

## 🔑 Configuração das API Keys

**IMPORTANTE**: Antes de usar os scripts, configure suas API Keys no arquivo `.env`:

```bash
# Copiar arquivo de exemplo
cp env_example.txt .env

# Editar com suas chaves
OPENAI_API_KEY=sk-your-openai-api-key-here
GEMINI_API_KEY=your-gemini-api-key-here
```

### Obter API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Gemini**: https://makersuite.google.com/app/apikey

### Testar configuração

```bash
python testar_configuracao.py
```

## Instalação

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

## 📖 Como Usar

### 🚀 Início Rápido (Recomendado)

#### 1. Testar configuração

```bash
python testar_configuracao.py
```

#### 2. Executar interface web

```bash
streamlit run app.py
```

#### 3. Usar a interface

1. Acesse http://localhost:8501
2. Verifique status das API Keys na sidebar
3. Faça upload do arquivo Excel
4. Configure parâmetros conforme necessário
5. Clique em "Processar Arquivo"
6. Acompanhe progresso em tempo real
7. Baixe o resultado processado

### 📋 Preparar Arquivos

#### Para Melhorador de Descrições

Crie uma planilha Excel com estas colunas:

| Coluna    | Obrigatória | Descrição                  |
| --------- | ----------- | -------------------------- |
| Título    | ✅          | Nome/título do produto     |
| Descrição | ✅          | Descrição atual do produto |
| Preço     | ❌          | Preço do produto           |
| SKU       | ❌          | Código SKU do produto      |
| Categoria | ❌          | Categoria do produto       |
| Marca     | ❌          | Marca do produto           |

#### Para Validador de Redirecionamentos

Crie uma planilha Excel com estas colunas:

| Coluna     | Obrigatória | Descrição                 |
| ---------- | ----------- | ------------------------- |
| URL Antiga | ✅          | URL que deve redirecionar |
| URL Nova   | ✅          | URL de destino esperada   |

### 🛠️ Uso via Linha de Comando

#### Melhorador de Descrições

```bash
# Com OpenAI
python product_description_enhancer.py catalogo.xlsx -p openai

# Com Gemini
python product_description_enhancer.py catalogo.xlsx -p gemini

# Opções avançadas
python product_description_enhancer.py catalogo.xlsx -p openai -m gpt-4 -r 2.0 -o resultado.xlsx
```

#### Validador de Redirecionamentos

```bash
# Validação básica
python redirect_validator.py urls.xlsx

# Opções avançadas
python redirect_validator.py urls.xlsx -o resultado.xlsx -t 15 -r 3
```

### 🧪 Scripts de Ajuda

#### Criar arquivo de exemplo

```bash
python criar_exemplo.py
```

#### Testar configuração

```bash
python testar_configuracao.py
```

### 📊 Opções de Configuração

#### Melhorador de Descrições

- `-p, --provider`: Provedor de IA (openai, gemini)
- `-m, --model`: Modelo específico (gpt-3.5-turbo, gpt-4, gemini-pro)
- `-r, --ratio`: Razão mínima descrição/título (padrão: 1.5)
- `-o, --output`: Arquivo de saída
- `-k, --api-key`: API Key (ou use variável de ambiente)

#### Validador de Redirecionamentos

- `-o, --output`: Arquivo de saída
- `-t, --timeout`: Timeout em segundos (padrão: 10)
- `-r, --max-redirects`: Máximo de redirecionamentos (padrão: 5)

### 🚀 Deploy na AWS (Produção)

#### 1. Pré-requisitos

```bash
# Instalar ferramentas AWS
pip install awscli awsebcli

# Configurar AWS CLI
aws configure
```

#### 2. Deploy automático

```bash
# Linux/Mac
./deploy.sh

# Windows
python deploy.py
```

#### 3. Deploy manual

```bash
# Inicializar aplicação
eb init compra-agora-script --platform python-3.11

# Criar ambiente
eb create compra-agora-env --instance-type t3.micro

# Deploy
eb deploy compra-agora-env
```

#### 4. Configurar variáveis de ambiente

No console AWS Elastic Beanstalk:

- Configuration → Software → Environment Properties
- Adicionar: `OPENAI_API_KEY`, `GEMINI_API_KEY`

#### 5. Documentação completa

Consulte o arquivo `AWS_DEPLOY_GUIDE.md` para instruções detalhadas.

## 📊 Resultados

### Validador de Redirecionamentos 301

O script irá adicionar as seguintes colunas à sua planilha:

- **Status**: "OK" (redirecionamento 301 correto) ou "NOK" (problema encontrado)
- **Código HTTP**: Código de status HTTP retornado
- **Observação**: Descrição detalhada do resultado

#### Exemplos de resultados:

| Status | Código HTTP | Observação                                                               |
| ------ | ----------- | ------------------------------------------------------------------------ |
| OK     | 301         | Redirecionamento 301 correto para https://exemplo.com/pagina-nova        |
| NOK    | 302         | Redirecionamento 302 (esperado 301) para https://exemplo.com/pagina-nova |
| NOK    | 404         | Sem redirecionamento (status 404)                                        |
| NOK    | TIMEOUT     | Timeout na requisição                                                    |

### Melhorador de Descrições de Produtos com SEO

O script irá adicionar as seguintes colunas à sua planilha:

- **Descrição_Melhorada**: Nova descrição gerada pela IA
- **Status_Melhoria**: "MELHORADO", "MANTIDO" ou "ERRO"
- **Motivo_Melhoria**: Razão pela qual foi melhorado ou mantido
- **Razão_Título_Descrição**: Razão entre tamanho da descrição e título
- **Meta_Title**: 🎯 Título otimizado para SEO (máx. 60 caracteres)
- **Meta_Description**: 📋 Descrição para resultados de busca (máx. 160 caracteres)

#### Exemplos de resultados:

| Título                        | Descrição Original        | Meta_Title                                   | Meta_Description                                                                             | Status_Melhoria |
| ----------------------------- | ------------------------- | -------------------------------------------- | -------------------------------------------------------------------------------------------- | --------------- |
| Smartphone Samsung Galaxy A54 | Smartphone Samsung        | Samsung Galaxy A54 \| Samsung - Compra Agora | Smartphone Samsung Galaxy A54 com câmera de 50MP e tela 6.4". Descubra e compre agora mesmo! | MELHORADO       |
| Produto com boa descrição     | Descrição já detalhada... | Nome Produto \| Marca - Compra Agora         | Descrição já detalhada com benefícios exclusivos. Experimente e aproveite!                   | MANTIDO         |

## 🔍 Regras de SEO Aplicadas

### Meta Title (Regras Obrigatórias do Compra Agora)

- **Comprimento**: Entre 50 e 60 caracteres
- **Estrutura**: "Nome Produto | Marca - Compra Agora"
- **Palavra-chave**: Principal no início sempre que possível
- **Marca**: Incluída no final
- **Sufixo**: "- Compra Agora" (15 caracteres)
- **Otimização**: Evitar keyword stuffing, ser claro e chamativo

### Meta Description (Regras Obrigatórias do Compra Agora)

- **Comprimento**: Entre 140 e 160 caracteres
- **Conteúdo**: Palavra-chave natural + explicação clara + benefícios
- **Gatilhos**: Incluir call-to-action efetivos
- **Diferenciais**: Destacar benefícios únicos
- **Unicidade**: Não duplicar entre páginas

### Preset do Niara

- **Meta Title**: tema/título + palavra-chave + audiência + tom de voz
- **Meta Description**: tema/título + palavra-chave + audiência + call_to_action + tom de voz

## Logs

O script gera logs detalhados em:

- Console (saída padrão)
- Arquivo `product_enhancer.log`

## Tratamento de Erros

O script trata automaticamente:

- URLs inválidas
- Timeouts de conexão
- Erros de rede
- Certificados SSL inválidos
- URLs vazias ou malformadas
- **Falhas na geração de meta tags (fallback automático)**

## 🎯 Exemplos de Uso Completo

### 🚀 Interface Streamlit (Mais Fácil)

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Testar configuração
python testar_configuracao.py

# 3. Executar interface
streamlit run app.py

# 4. Usar interface web
# Acesse http://localhost:8501
# Upload do arquivo → Configurar → Processar → Baixar
```

### 🛠️ Linha de Comando

#### Validador de Redirecionamentos

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar validação
python redirect_validator.py urls_para_validar.xlsx

# 3. Verificar resultados
# O arquivo será salvo como "urls_para_validar_validado.xlsx"
```

#### Melhorador de Descrições com SEO

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Criar arquivo de exemplo (opcional)
python criar_exemplo.py

# 3. Executar melhoria com SEO
python product_description_enhancer.py catalogo.xlsx -p openai

# 4. Verificar resultados
# O arquivo será salvo como "catalogo_melhorado.xlsx"
# Inclui Meta Title e Meta Description para todos os produtos
```

### 💻 Exemplo Python

```python
import os
from dotenv import load_dotenv
from product_description_enhancer import ProductDescriptionEnhancer, OpenAIProvider

# Carregar variáveis de ambiente
load_dotenv()

# Configurar provedor
api_key = os.getenv('OPENAI_API_KEY')
ai_provider = OpenAIProvider(api_key)
enhancer = ProductDescriptionEnhancer(ai_provider)

# Processar arquivo
enhancer.process_excel_file('catalogo.xlsx', 'resultado.xlsx')
```

## 📁 Estrutura do projeto

```
compra-agora-script/
├── app.py                           # 🆕 Interface Streamlit
├── application.py                   # 🆕 Ponto de entrada para AWS EBS
├── redirect_validator.py            # Validador de redirecionamentos
├── product_description_enhancer.py  # Melhorador de descrições + SEO
├── exemplo_uso.py                   # Exemplos do validador
├── exemplo_uso_com_env.py           # Exemplos com variáveis de ambiente
├── exemplo_uso_seo.py               # Exemplos das funcionalidades SEO
├── criar_exemplo.py                 # 🆕 Script para criar arquivo de exemplo
├── testar_configuracao.py          # 🆕 Script para testar configuração
├── deploy.sh                        # 🆕 Script de deploy (Linux/Mac)
├── deploy.py                        # 🆕 Script de deploy (Windows)
├── requirements.txt                 # Dependências (inclui Streamlit)
├── requirements-prod.txt            # 🆕 Dependências para produção
├── config.json                      # Configurações (inclui SEO)
├── env_example.txt                  # 🆕 Exemplo de configuração .env
├── .ebignore                        # 🆕 Arquivos ignorados no deploy
├── .ebextensions/                   # 🆕 Configurações AWS EBS
│   ├── 01_python.config
│   ├── 02_dependencies.config
│   └── 03_streamlit.config
├── STREAMLIT_GUIDE.md              # 🆕 Guia da interface Streamlit
├── AWS_DEPLOY_GUIDE.md             # 🆕 Guia completo de deploy AWS
├── README.md                        # Este arquivo
├── redirect_validator.log           # Logs do validador
└── product_enhancer.log             # Logs do melhorador
```

## ⚠️ Notas importantes

### Validador de Redirecionamentos

- O script faz pausas entre requisições para não sobrecarregar servidores
- URLs são normalizadas automaticamente (adiciona https:// se necessário)
- Certificados SSL são ignorados para facilitar testes
- O script simula um navegador real com headers apropriados

### Melhorador de Descrições com SEO

- Requer API key válida do OpenAI ou Google Gemini
- Faz pausas entre requisições para respeitar limites da API
- Descrições muito curtas (razão < 1.5) são automaticamente melhoradas
- **Meta Title e Meta Description são gerados para TODOS os produtos**
- **Fallback automático se a IA falhar na geração de meta tags**
- O script mantém a descrição original se não conseguir melhorar
- Logs detalhados são gerados para acompanhar o progresso
- **Configurações de SEO personalizáveis via config.json**

## 🚀 Benefícios das Novas Funcionalidades

### Para SEO

- **Melhor ranking** nos mecanismos de busca
- **Meta tags otimizadas** para cada produto
- **Palavras-chave** estrategicamente posicionadas
- **Estrutura consistente** em todo o catálogo

### Para Conversão

- **Títulos atrativos** que geram mais cliques
- **Descrições persuasivas** que convertem visitantes
- **Informações claras** sobre benefícios dos produtos
- **Chamadas para ação** efetivas

### Para Produtividade

- **Automação completa** do processo de SEO
- **Processamento em lote** de catálogos inteiros
- **Qualidade consistente** em todos os produtos
- **Tempo economizado** na otimização manual
