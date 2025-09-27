# 🚀 Interface Streamlit - Melhorador de Descrições de Produtos

## 📋 Como Executar a Aplicação

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a Aplicação

```bash
streamlit run app.py
```

### 3. Acessar a Interface

A aplicação será aberta automaticamente no seu navegador em:

- **URL Local**: http://localhost:8501
- **URL de Rede**: http://192.168.x.x:8501 (para acesso de outros dispositivos)

## 🎯 Funcionalidades da Interface

### ✅ Upload de Arquivos

- Suporte a arquivos Excel (.xlsx, .xls)
- Validação automática de colunas necessárias
- Preview dos dados antes do processamento

### ⚙️ Configurações

- **Provedor de IA**: OpenAI GPT ou Google Gemini (baseado nas API Keys configuradas)
- **API Key**: Lida automaticamente do arquivo .env
- **Modelo**: Seleção do modelo específico
- **Razão mínima**: Controle da sensibilidade para melhorar descrições
- **Configurações avançadas**: Frases proibidas, limites de caracteres

### 📊 Monitoramento em Tempo Real

- **Barra de progresso**: Acompanha o processamento produto por produto
- **Status em tempo real**: Mostra qual produto está sendo processado
- **Logs detalhados**: Captura todos os logs do processamento
- **Estatísticas**: Contadores de produtos processados, melhorados, mantidos e erros

### 📋 Visualização de Resultados

- **Tabela interativa**: Visualização dos resultados com filtros
- **Filtros por status**: Melhorado, Mantido, Erro
- **Seleção de colunas**: Escolha quais colunas visualizar
- **Download**: Baixar arquivo processado em Excel

## 🔧 Configurações Avançadas

### Frases Proibidas

Configure frases que não devem aparecer nas descrições geradas:

```
margem
lucro
margem de lucro
clientes frescos
```

### Limites de Caracteres

- **Mínimo**: Comprimento mínimo da descrição melhorada
- **Máximo**: Comprimento máximo da descrição melhorada

## 📁 Estrutura de Arquivos Esperada

O arquivo Excel deve conter pelo menos estas colunas:

| Coluna    | Obrigatória | Descrição                  |
| --------- | ----------- | -------------------------- |
| Título    | ✅          | Nome/título do produto     |
| Descrição | ✅          | Descrição atual do produto |
| Preço     | ❌          | Preço do produto           |
| SKU       | ❌          | Código SKU do produto      |
| Categoria | ❌          | Categoria do produto       |
| Marca     | ❌          | Marca do produto           |

## 🔑 Configuração das API Keys

### 1. Criar arquivo .env

Crie um arquivo `.env` na raiz do projeto com suas API Keys:

```bash
# Para OpenAI
OPENAI_API_KEY=sk-your-openai-api-key-here

# Para Gemini (opcional)
GEMINI_API_KEY=your-gemini-api-key-here
```

### 2. Obter API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Gemini**: https://makersuite.google.com/app/apikey

### 3. Verificar configuração

A interface mostrará o status das API Keys na sidebar:

- ✅ Verde: API Key configurada
- ❌ Vermelho: API Key não encontrada

### 4. Arquivo de exemplo

Use o arquivo `env_example.txt` como referência para criar seu `.env`.

## 🎨 Interface Visual

### Cores e Estilos

- **Header principal**: Azul com ícone de foguete
- **Status boxes**: Cores diferenciadas para sucesso, erro e informação
- **Logs**: Container com scroll e fonte monospace
- **Layout**: Sidebar para configurações, área principal para upload e resultados

### Responsividade

- Interface adaptável para diferentes tamanhos de tela
- Layout em colunas para melhor organização
- Componentes otimizados para mobile e desktop

## 🔍 Troubleshooting

### Problemas Comuns

1. **Erro de API Key**

   - Verifique se o arquivo .env existe na raiz do projeto
   - Confirme se a chave está correta no arquivo .env
   - Verifique se tem créditos disponíveis
   - Teste com um arquivo pequeno primeiro

2. **Arquivo não carrega**

   - Verifique se é um arquivo Excel válido
   - Confirme se tem as colunas necessárias
   - Tente com um arquivo menor

3. **Processamento lento**

   - Reduza o número de produtos
   - Use modelo mais rápido (gpt-3.5-turbo)
   - Verifique conexão com internet

4. **Erro de memória**
   - Processe arquivos menores
   - Reinicie a aplicação
   - Verifique recursos do sistema

## 🚀 Dicas de Uso

### Para Melhores Resultados

1. **Use arquivos menores** para testes iniciais
2. **Configure frases proibidas** específicas do seu negócio
3. **Ajuste a razão mínima** baseado na qualidade das suas descrições
4. **Monitore os logs** para identificar problemas
5. **Teste diferentes modelos** para encontrar o melhor resultado

### Performance

- **OpenAI GPT-3.5-turbo**: Mais rápido e econômico
- **OpenAI GPT-4**: Melhor qualidade, mais lento e caro
- **Gemini Pro**: Alternativa gratuita com boa qualidade

## 📞 Suporte

Para problemas ou dúvidas:

1. Verifique os logs da aplicação
2. Consulte a documentação do script original
3. Teste com arquivos menores
4. Verifique configurações de API
