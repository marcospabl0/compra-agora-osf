# 📦 Guia Completo - Processamento em Lotes

## 🤔 **O que significa "100 produtos por lote"?**

### 📊 **Definição Simples**

"100 produtos por lote" significa que você deve processar **máximo 100 produtos por vez** na interface web, em vez de tentar processar um catálogo inteiro de milhares de produtos de uma só vez.

### 🎯 **Analogia do Mundo Real**

Imagine que você tem 1000 livros para catalogar:

- ❌ **Tentar catalogar todos de uma vez**: Pode levar horas, cansar, cometer erros
- ✅ **Catalogar em grupos de 100**: Mais organizado, menos cansativo, menos erros

## 🔍 **Por que essa limitação existe?**

### 1. **Limitações do Streamlit Cloud**

- ⏱️ **Timeout**: Máximo 10 minutos por sessão
- 💾 **Memória**: Máximo 1GB de RAM
- 🔄 **CPU**: Recursos limitados para processamento intensivo
- 🌐 **Rede**: Limitações de requisições para APIs externas

### 2. **Limitações das APIs de IA**

- 🚦 **Rate Limits**: OpenAI e Gemini têm limites de requisições por minuto
- 💰 **Custos**: Processar muitos produtos pode gerar custos altos
- ⚡ **Performance**: Requisições simultâneas podem causar lentidão

### 3. **Experiência do Usuário**

- 📱 **Interface**: Mais responsiva com menos produtos
- 🔄 **Feedback**: Progresso mais claro e detalhado
- 🛡️ **Segurança**: Menor risco de perder dados por timeout

## 📈 **Exemplo Prático**

### ❌ **Processamento Incorreto**

```
Arquivo Excel com 1000 produtos
↓
Tentar processar todos de uma vez
↓
❌ Timeout após 10 minutos
❌ Erro de memória
❌ Rate limit da API
❌ Usuário frustrado
```

### ✅ **Processamento Correto**

```
Arquivo Excel com 1000 produtos
↓
Dividir em 10 lotes de 100 produtos cada
↓
Processar lote 1: produtos 1-100 ✅
Processar lote 2: produtos 101-200 ✅
Processar lote 3: produtos 201-300 ✅
...
Processar lote 10: produtos 901-1000 ✅
↓
🎉 Todos os produtos processados com sucesso!
```

## 🛠️ **Como Implementar Processamento em Lotes**

### 1. **Detecção Automática de Arquivos Grandes**

```python
def verificar_tamanho_arquivo(df):
    total_produtos = len(df)

    if total_produtos > 100:
        st.warning(f"⚠️ Arquivo grande: {total_produtos} produtos")
        st.info("💡 Recomendamos processar em lotes de 100 produtos")
        return True
    return False
```

### 2. **Divisão em Lotes**

```python
def dividir_em_lotes(df, tamanho_lote=100):
    lotes = []
    for i in range(0, len(df), tamanho_lote):
        lote = df.iloc[i:i + tamanho_lote].copy()
        lotes.append(lote)
    return lotes
```

### 3. **Processamento Sequencial**

```python
def processar_todos_lotes(lotes):
    resultados = []

    for i, lote in enumerate(lotes, 1):
        st.info(f"🔄 Processando lote {i}/{len(lotes)}")

        # Processar lote
        resultado = processar_lote(lote)
        resultados.append(resultado)

        # Pausa entre lotes
        if i < len(lotes):
            time.sleep(5)  # Evitar rate limits

    return pd.concat(resultados)
```

## 📊 **Tamanhos de Lote Recomendados**

### 🎯 **Por Tipo de Arquivo**

| Tamanho do Arquivo | Tamanho do Lote | Tempo Estimado |
| ------------------ | --------------- | -------------- |
| 1-50 produtos      | 50              | 2-5 minutos    |
| 51-200 produtos    | 100             | 5-10 minutos   |
| 201-500 produtos   | 100             | 10-20 minutos  |
| 501-1000 produtos  | 100             | 20-40 minutos  |
| 1000+ produtos     | 100             | 40+ minutos    |

### ⚡ **Por Provedor de IA**

| Provedor | Modelo            | Lote Recomendado | Razão                 |
| -------- | ----------------- | ---------------- | --------------------- |
| OpenAI   | gpt-3.5-turbo     | 100              | Mais rápido           |
| OpenAI   | gpt-4             | 50               | Mais lento, mais caro |
| Gemini   | gemini-pro        | 100              | Balanceado            |
| Gemini   | gemini-pro-vision | 50               | Mais lento            |

## 🎮 **Interface do Usuário**

### 1. **Detecção Automática**

```
📁 Upload do arquivo
↓
🔍 Verificar tamanho
↓
📊 Mostrar informações:
   - Total de produtos: 1000
   - Lotes necessários: 10
   - Tempo estimado: 30 minutos
```

### 2. **Opções de Processamento**

```
┌─────────────────────────────────────┐
│ 📦 Processar em Lotes (Recomendado) │
│ ⚡ Processar Tudo (Risco de Timeout)│
└─────────────────────────────────────┘
```

### 3. **Progresso Visual**

```
🔄 Processando lote 3/10
├─ Produto 201/300
├─ ⏱️ Tempo restante: 5 minutos
└─ 📊 Progresso: 30%
```

## 💡 **Dicas de Otimização**

### 1. **Escolha o Modelo Certo**

- **Para velocidade**: gpt-3.5-turbo
- **Para qualidade**: gpt-4 (mas use lotes menores)

### 2. **Configure Pausas Entre Lotes**

```python
# Pausa de 5 segundos entre lotes
time.sleep(5)

# Pausa maior para APIs com rate limit baixo
time.sleep(10)
```

### 3. **Monitore o Progresso**

```python
# Mostrar progresso detalhado
st.progress(lote_atual / total_lotes)
st.info(f"Lote {lote_atual}/{total_lotes} - {produtos_processados} produtos")
```

### 4. **Salve Resultados Parciais**

```python
# Salvar resultado de cada lote
resultado_lote.to_excel(f"lote_{numero_lote}.xlsx")

# Combinar no final
resultado_final = pd.concat(todos_lotes)
```

## 🚨 **Problemas Comuns e Soluções**

### ❌ **Timeout**

**Problema**: Lote muito grande
**Solução**: Reduza para 50 produtos por lote

### ❌ **Rate Limit**

**Problema**: Muitas requisições muito rápido
**Solução**: Aumente a pausa entre lotes para 10 segundos

### ❌ **Memória Insuficiente**

**Problema**: Arquivo muito grande
**Solução**: Processe lotes menores (25-50 produtos)

### ❌ **Custos Altos**

**Problema**: Usando modelo caro (gpt-4)
**Solução**: Use gpt-3.5-turbo para lotes grandes

## 📋 **Checklist para Processamento em Lotes**

### ✅ **Antes de Começar**

- [ ] Arquivo Excel preparado com colunas corretas
- [ ] API Key configurada e com créditos
- [ ] Tamanho do arquivo verificado
- [ ] Tamanho do lote definido (recomendado: 100)

### ✅ **Durante o Processamento**

- [ ] Monitorar progresso de cada lote
- [ ] Verificar se não há erros de API
- [ ] Aguardar pausas entre lotes
- [ ] Salvar resultados parciais

### ✅ **Após o Processamento**

- [ ] Combinar todos os lotes
- [ ] Verificar qualidade dos resultados
- [ ] Baixar arquivo final
- [ ] Revisar estatísticas de processamento

## 🎯 **Exemplo Completo**

### **Cenário**: Arquivo com 500 produtos

```
1. 📁 Upload do arquivo
2. 🔍 Detecção: 500 produtos → 5 lotes de 100
3. ⚙️ Configuração: gpt-3.5-turbo, lote de 100
4. 🚀 Processamento:
   - Lote 1: produtos 1-100 (5 min)
   - Lote 2: produtos 101-200 (5 min)
   - Lote 3: produtos 201-300 (5 min)
   - Lote 4: produtos 301-400 (5 min)
   - Lote 5: produtos 401-500 (5 min)
5. 📊 Resultado: 500 produtos processados em 25 minutos
6. 📥 Download: arquivo_final.xlsx
```

## 🆘 **Suporte**

Se encontrar problemas com processamento em lotes:

1. **Verifique o tamanho do lote** (recomendado: 100)
2. **Confirme as pausas entre lotes** (5-10 segundos)
3. **Monitore o uso da API** para evitar rate limits
4. **Use modelos mais rápidos** para lotes grandes

---

**💡 Lembre-se**: Processamento em lotes é uma estratégia de **qualidade** e **confiabilidade**, não uma limitação!
