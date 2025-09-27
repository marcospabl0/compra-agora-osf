# 🚀 Guia Completo - Deploy no Streamlit Community Cloud

## 📋 Pré-requisitos

- ✅ Conta no GitHub
- ✅ Conta no Streamlit Cloud (gratuita)
- ✅ API Key do OpenAI ou Google Gemini
- ✅ Repositório do projeto no GitHub

## 🔧 Passo a Passo

### 1. **Preparar o Repositório GitHub**

```bash
# 1. Fazer fork do repositório original
# 2. Clonar seu fork
git clone https://github.com/SEU_USUARIO/compra-agora-osf.git
cd compra-agora-osf

# 3. Verificar se todos os arquivos estão presentes
ls -la
# Deve conter:
# - app.py
# - product_description_enhancer.py
# - config.json
# - requirements-streamlit-cloud.txt
# - .streamlit/config.toml
# - exemplo_catalogo_streamlit.xlsx
```

### 2. **Configurar Secrets no Streamlit Cloud**

1. **Acesse**: [share.streamlit.io](https://share.streamlit.io)
2. **Faça login** com sua conta GitHub
3. **Clique em "New app"**
4. **Configure o repositório**:
   - Repository: `SEU_USUARIO/compra-agora-osf`
   - Branch: `main` (ou `master`)
   - Main file path: `app.py`
5. **Antes de clicar em Deploy**, clique em **"Advanced settings"**
6. **Configure os Secrets**:

```toml
# Cole este conteúdo na área de Secrets:
OPENAI_API_KEY = "sk-your-openai-api-key-here"
GEMINI_API_KEY = "your-gemini-api-key-here"
```

7. **Clique em "Deploy"**

### 3. **Verificar o Deploy**

Após o deploy (pode levar 2-5 minutos):

1. **Acesse a URL** gerada pelo Streamlit Cloud
2. **Verifique se a aplicação carrega** corretamente
3. **Teste o upload** do arquivo de exemplo
4. **Verifique se as API Keys** aparecem como configuradas na sidebar

## 🧪 Teste Local (Opcional)

Para testar localmente antes do deploy:

```bash
# 1. Instalar dependências
pip install -r requirements-streamlit-cloud.txt

# 2. Configurar variáveis de ambiente
cp env_example.txt .env
# Edite o arquivo .env com suas API Keys

# 3. Executar localmente
streamlit run app.py

# 4. Acessar http://localhost:8501
```

## 🔍 Solução de Problemas Comuns

### ❌ Erro: "ModuleNotFoundError"

**Causa**: Dependências não instaladas
**Solução**: Verifique se `requirements-streamlit-cloud.txt` está correto

### ❌ Erro: "API Key not found"

**Causa**: Secrets não configurados
**Solução**: Verifique se as API Keys estão nas Secrets do Streamlit Cloud

### ❌ Erro: "Timeout"

**Causa**: Processamento muito longo
**Solução**: Use arquivos menores ou modelos mais rápidos

### ❌ Erro: "File upload failed"

**Causa**: Arquivo muito grande ou formato incorreto
**Solução**: Use arquivos Excel (.xlsx) menores que 200MB

## 📊 Monitoramento

### Logs do Streamlit Cloud

1. **Acesse** o painel do seu app no Streamlit Cloud
2. **Clique em "Logs"** para ver erros e informações
3. **Monitore** o uso de recursos

### Métricas de Performance

- **Tempo de resposta**: < 30 segundos para uploads pequenos
- **Uso de memória**: < 1GB
- **Timeout**: Máximo 10 minutos por sessão

## 🚀 Otimizações para Produção

### 1. **Limitar Tamanho de Arquivos**

```python
# No app.py, adicione validação:
if uploaded_file.size > 50 * 1024 * 1024:  # 50MB
    st.error("Arquivo muito grande. Máximo 50MB.")
    return
```

### 2. **Cache de Resultados**

```python
# Use @st.cache_data para cache
@st.cache_data
def process_data(df):
    # Processamento aqui
    return result
```

### 3. **Progresso Otimizado**

```python
# Use st.progress com updates menores
for i in range(total):
    progress_bar.progress(i / total)
    # Processar item
```

## 📈 Próximos Passos

Após o deploy bem-sucedido:

1. **Compartilhe a URL** com sua equipe
2. **Teste com dados reais** do Compra Agora
3. **Monitore o uso** e performance
4. **Colete feedback** dos usuários
5. **Implemente melhorias** baseadas no uso

## 🆘 Suporte

Se encontrar problemas:

1. **Verifique os logs** no Streamlit Cloud
2. **Teste localmente** primeiro
3. **Consulte a documentação** do Streamlit
4. **Entre em contato** com o suporte técnico

---

**🎉 Parabéns! Sua aplicação está no ar!**

Acesse: `https://SEU_USUARIO-compra-agora-osf-app-xxxxx.streamlit.app`
