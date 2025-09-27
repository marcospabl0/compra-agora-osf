# 🚀 Compra Agora - Melhorador de Descrições com SEO

## 📋 Sobre o Projeto

Esta é uma aplicação Streamlit para **melhorar descrições de produtos** usando Inteligência Artificial (OpenAI GPT ou Google Gemini) e **gerar Meta Title e Meta Description otimizados para SEO**.

### ✨ Funcionalidades Principais

- 🤖 **Melhoria automática de descrições** usando IA
- 🎯 **Geração de Meta Title e Meta Description** otimizados para SEO
- 🧹 **Limpeza automática de títulos** (remove volume, peso, cor, tamanho)
- 📊 **Interface web interativa** com upload de arquivos Excel
- ⚡ **Processamento em tempo real** com logs detalhados
- 📥 **Download automático** dos resultados processados

## 🔧 Configuração para Streamlit Cloud

### 1. **Fork do Repositório**

```bash
# Faça fork deste repositório no GitHub
# Clone seu fork localmente
git clone https://github.com/SEU_USUARIO/compra-agora-osf.git
cd compra-agora-osf
```

### 2. **Configurar Secrets no Streamlit Cloud**

No painel do Streamlit Cloud, vá em **Settings** → **Secrets** e adicione:

```toml
# Para OpenAI
OPENAI_API_KEY = "sk-your-openai-api-key-here"

# Para Google Gemini (opcional)
GEMINI_API_KEY = "your-gemini-api-key-here"
```

### 3. **Deploy no Streamlit Cloud**

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Conecte sua conta GitHub
3. Selecione o repositório `compra-agora-osf`
4. Configure:
   - **Main file path**: `app.py`
   - **Requirements file**: `requirements-streamlit-cloud.txt`
5. Clique em **Deploy**

## 📁 Estrutura de Arquivos

```
compra-agora-osf/
├── app.py                              # 🎯 Aplicação principal Streamlit
├── product_description_enhancer.py     # 🤖 Motor de IA e SEO
├── config.json                         # ⚙️ Configurações SEO
├── requirements-streamlit-cloud.txt    # 📦 Dependências para Cloud
├── .streamlit/
│   └── config.toml                     # 🎨 Configurações Streamlit
├── exemplo_catalogo_streamlit.xlsx     # 📊 Arquivo de exemplo
└── README_STREAMLIT_CLOUD.md           # 📖 Este arquivo
```

## 🎯 Como Usar

### 1. **Preparar Arquivo Excel**

Crie uma planilha Excel com estas colunas:

| Coluna    | Obrigatória | Descrição                  |
| --------- | ----------- | -------------------------- |
| Título    | ✅          | Nome/título do produto     |
| Descrição | ✅          | Descrição atual do produto |
| Preço     | ❌          | Preço do produto           |
| SKU       | ❌          | Código SKU do produto      |
| Categoria | ❌          | Categoria do produto       |
| Marca     | ❌          | Marca do produto           |

### 2. **Usar a Interface**

1. **Acesse a aplicação** no Streamlit Cloud
2. **Verifique o status** das API Keys na sidebar
3. **Faça upload** do arquivo Excel
4. **Configure parâmetros** conforme necessário:
   - Provedor de IA (OpenAI ou Gemini)
   - Modelo específico
   - Razão mínima descrição/título
5. **Clique em "Processar Arquivo"**
6. **Acompanhe o progresso** em tempo real
7. **Baixe o resultado** processado

## 🔑 Obter API Keys

### OpenAI

1. Acesse [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Crie uma nova API Key
3. Adicione créditos à sua conta

### Google Gemini

1. Acesse [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Crie uma nova API Key
3. Configure no Streamlit Cloud

## 📊 Resultados Gerados

O processamento adiciona estas colunas ao seu arquivo:

- **Descrição_Melhorada**: Nova descrição gerada pela IA
- **Status_Melhoria**: "MELHORADO", "MANTIDO" ou "ERRO"
- **Motivo_Melhoria**: Razão da melhoria ou manutenção
- **Razão_Título_Descrição**: Razão entre tamanho da descrição e título
- **Meta_Title**: 🎯 Título otimizado para SEO (máx. 60 caracteres)
- **Meta_Description**: 📋 Descrição para resultados de busca (máx. 160 caracteres)

## 🎯 Regras de SEO Aplicadas

### Meta Title

- **Comprimento**: 50-60 caracteres
- **Formato**: "Nome Produto | Marca - Compra Agora"
- **Palavra-chave**: Principal no início
- **Sufixo obrigatório**: "- Compra Agora"

### Meta Description

- **Comprimento**: 140-160 caracteres
- **Conteúdo**: Palavra-chave natural + explicação + benefícios
- **Gatilhos**: Call-to-action efetivos
- **Diferenciais**: Benefícios únicos destacados

## 🚀 Exemplo de Uso

### Antes (Descrição Curta)

```
Título: Smartphone Samsung Galaxy A54 128GB Azul
Descrição: Smartphone Samsung
```

### Depois (Melhorado com SEO)

```
Título: Smartphone Samsung Galaxy A54
Descrição: Smartphone Samsung Galaxy A54 com câmera de 50MP, tela Super AMOLED de 6.4" e bateria de 5000mAh. Desempenho excepcional com processador Exynos 1380 e 128GB de armazenamento. Perfeito para fotos profissionais e multitarefas intensivas. Descubra a tecnologia Samsung em suas mãos!

Meta Title: Samsung Galaxy A54 | Samsung - Compra Agora
Meta Description: Smartphone Samsung Galaxy A54 com câmera 50MP e tela 6.4". Desempenho excepcional e bateria duradoura. Descubra e compre agora mesmo!
```

## ⚠️ Limitações do Streamlit Cloud

- **Timeout**: Processamento limitado a 10 minutos
- **Memória**: Máximo 1GB de RAM
- **Arquivos**: Upload limitado a 200MB
- **CPU**: Limitado para processamento intensivo

### 💡 Dicas para Otimizar

1. **Processe lotes menores** (máximo 50-100 produtos por vez)
2. **Use modelos mais rápidos** (gpt-3.5-turbo em vez de gpt-4)
3. **Monitore o uso de API** para evitar limites de rate
4. **Teste primeiro** com arquivos pequenos

## 🔧 Solução de Problemas

### Erro de API Key

- Verifique se as secrets estão configuradas corretamente
- Confirme se a API Key é válida e tem créditos

### Timeout de Processamento

- Reduza o número de produtos por lote
- Use modelos mais rápidos
- Verifique a conexão com a internet

### Erro de Upload

- Verifique se o arquivo é Excel (.xlsx)
- Confirme se tem as colunas obrigatórias
- Reduza o tamanho do arquivo

## 📞 Suporte

Para dúvidas ou problemas:

- 📧 Email: suporte@compraagora.com.br
- 💬 Discord: [Link do servidor]
- 📖 Documentação: [Link da documentação]

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**Desenvolvido com ❤️ para o Compra Agora**
