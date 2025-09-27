#!/usr/bin/env python3
"""
Script para melhorar descrições de produtos usando IA.
Processa um catálogo de produtos e usa OpenAI/Gemini para criar descrições mais detalhadas
quando a descrição atual é muito curta (similar ao tamanho do título).
Agora também gera Meta Title e Meta Description otimizados para SEO.
"""

import pandas as pd
import openai
import google.generativeai as genai
import time
import logging
import json
import os
import re
import difflib
import unicodedata
from typing import Optional, Dict, Any, Tuple, List
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('product_enhancer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ProductInfo:
    """Informações do produto para processamento."""
    title: str
    description: str
    price: Optional[str] = None
    sku: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None

@dataclass
class SEOInfo:
    """Informações SEO geradas para o produto."""
    meta_title: str
    meta_description: str
    enhanced_description: str

def clean_product_title(title: str) -> str:
    """
    Remove informações de volume, apresentação e especificações técnicas do título do produto.
    
    Args:
        title: Título original do produto
        
    Returns:
        Título limpo sem especificações técnicas
    """
    if not title:
        return title
    
    # Padrões para remover (volume, apresentação, especificações técnicas)
    patterns_to_remove = [
        # Volumes e medidas
        r'\b\d+(?:\.\d+)?\s*(?:ml|mL|ML|L|l|g|kg|cm|mm|pol|")\b',
        r'\b\d+(?:\.\d+)?\s*(?:mililitros?|litros?|gramas?|quilos?|centímetros?|milímetros?|polegadas?)\b',
        
        # Apresentações e embalagens
        r'\b(?:pacote|pack|kit|conjunto|set|caixa|frasco|garrafa|lata|pote|tubo|sachê|sache|sachê|sache)\b',
        r'\b(?:de\s+\d+|\d+\s+unidades?|\d+\s+peças?)\b',
        
        # Especificações técnicas comuns
        r'\b(?:edição\s+(?:limitada|especial|premium|exclusiva))\b',
        r'\b(?:versão\s+(?:plus|pro|max|ultra|premium))\b',
        r'\b(?:modelo\s+\d+[A-Za-z]*)\b',
        r'\b(?:série\s+[A-Za-z0-9]+)\b',
        
        # Informações de cor quando não essenciais
        r'\b(?:cor\s+(?:azul|vermelha|verde|amarela|preta|branca|rosa|laranja|roxo|marrom|cinza))\b',
        r'\b(?:azul|vermelho|verde|amarelo|preto|branco|rosa|laranja|roxo|marrom|cinza)\s+(?:claro|escuro|clara|escura)?\b',
        
        # Tamanhos quando não essenciais para o produto
        r'\b(?:tamanho\s+(?:P|M|G|GG|XG|PP|P|M|G|GG|XG|PP))\b',
        r'\b(?:P|M|G|GG|XG|PP)\b',
        
        # Outras especificações técnicas
        r'\b(?:tipo\s+[A-Za-z]+)\b',
        r'\b(?:categoria\s+[A-Za-z]+)\b',
        r'\b(?:linha\s+[A-Za-z]+)\b',
        r'\b(?:coleção\s+[A-Za-z]+)\b',
        
        # Informações de peso/volume específicas
        r'\b(?:peso\s+\d+(?:\.\d+)?\s*(?:g|kg))\b',
        r'\b(?:capacidade\s+\d+(?:\.\d+)?\s*(?:ml|L|g|kg))\b',
        
        # Informações de dimensões
        r'\b(?:dimensões?\s+\d+(?:\.\d+)?\s*x\s*\d+(?:\.\d+)?\s*(?:cm|mm|pol))\b',
        
        # Informações de quantidade em embalagens
        r'\b(?:contém\s+\d+(?:\.\d+)?\s*(?:unidades?|peças?|comprimidos?|cápsulas?))\b',
        r'\b(?:quantidade\s+\d+(?:\.\d+)?\s*(?:ml|g|unidades?))\b',
        
        # Melhorias específicas baseadas no teste
        r'\b(?:peso|capacidade|dimensões?|contém|quantidade)\b',
        r'\b(?:polegadas?)\b',
        r'\b(?:edição|versão|modelo|série|cor|tamanho|tipo|categoria|linha|coleção)\b'
    ]
    
    # Aplicar todos os padrões
    cleaned_title = title
    for pattern in patterns_to_remove:
        cleaned_title = re.sub(pattern, '', cleaned_title, flags=re.IGNORECASE)
    
    # Limpar espaços extras e caracteres especiais
    cleaned_title = re.sub(r'\s+', ' ', cleaned_title)  # Múltiplos espaços
    cleaned_title = re.sub(r'^\s+|\s+$', '', cleaned_title)  # Espaços no início/fim
    cleaned_title = re.sub(r'[,\s]+$', '', cleaned_title)  # Vírgulas e espaços no final
    cleaned_title = re.sub(r'^\s*[,\s]+', '', cleaned_title)  # Vírgulas e espaços no início
    
    # Se o título ficou muito curto, usar o original
    if len(cleaned_title.strip()) < 3:
        logger.warning(f"Título limpo ficou muito curto para '{title}', mantendo original")
        return title
    
    return cleaned_title.strip()

def clean_markdown_formatting(text: str) -> str:
    """
    Remove formatação Markdown do texto retornado pela IA.
    
    Args:
        text: Texto com possível formatação Markdown
        
    Returns:
        Texto limpo sem formatação Markdown
    """
    if not text:
        return text
    
    # Remover formatação Markdown comum
    cleaned_text = text
    
    # Remover blocos de código ``` primeiro (para evitar conflitos)
    cleaned_text = re.sub(r'```.*?```', '', cleaned_text, flags=re.DOTALL)
    
    # Remover negrito **texto** ou __texto__
    cleaned_text = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned_text)
    cleaned_text = re.sub(r'__(.*?)__', r'\1', cleaned_text)
    
    # Remover itálico *texto* ou _texto_
    cleaned_text = re.sub(r'\*(.*?)\*', r'\1', cleaned_text)
    cleaned_text = re.sub(r'_(.*?)_', r'\1', cleaned_text)
    
    # Remover código `texto`
    cleaned_text = re.sub(r'`(.*?)`', r'\1', cleaned_text)
    
    # Remover links [texto](url)
    cleaned_text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', cleaned_text)
    
    # Remover cabeçalhos # ## ### #### (preservando quebras de linha)
    cleaned_text = re.sub(r'^#{1,6}\s*', '', cleaned_text, flags=re.MULTILINE)
    
    # Remover listas - * - - item (preservando quebras de linha)
    cleaned_text = re.sub(r'^[\s]*[-*+]\s*', '', cleaned_text, flags=re.MULTILINE)
    
    # Remover numeração 1. 2. 3. (preservando quebras de linha)
    cleaned_text = re.sub(r'^[\s]*\d+\.\s*', '', cleaned_text, flags=re.MULTILINE)
    
    # Limpar espaços extras mas preservar quebras de linha únicas
    cleaned_text = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_text)  # Múltiplas quebras de linha -> dupla
    cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)  # Múltiplos espaços/tabs -> espaço único
    cleaned_text = cleaned_text.strip()
    
    return cleaned_text

def filter_prohibited_content(description: str, prohibited_phrases: List[str] = None) -> str:
    """
    Remove ou substitui frases/palavras proibidas da descrição.
    
    Args:
        description: Descrição a ser filtrada
        prohibited_phrases: Lista de frases/palavras proibidas
        
    Returns:
        Descrição filtrada
    """
    if not description or not prohibited_phrases:
        return description
    
    filtered_desc = description
    
    # Lista padrão de textos proibidos (pode ser expandida)
    default_prohibited = [
        "compre já",
        "compre agora", 
        "adquira já",
        "adquira agora",
        "não perca",
        "oferta imperdível",
        "promoção",
        "desconto",
        "preço baixo",
        "melhor preço",
        "frete grátis",
        "entrega grátis"
    ]
    
    # Combinar listas
    all_prohibited = list(set(default_prohibited + (prohibited_phrases or [])))
    
    # Remover frases proibidas (case insensitive)
    for phrase in all_prohibited:
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        filtered_desc = pattern.sub('', filtered_desc)
    
    # Limpar espaços extras e pontuação órfã
    filtered_desc = re.sub(r'\s+', ' ', filtered_desc)
    filtered_desc = re.sub(r'\s*[,;.!?]\s*[,;.!?]+', '.', filtered_desc)
    filtered_desc = re.sub(r'^\s*[,;.!?]+\s*', '', filtered_desc)
    filtered_desc = filtered_desc.strip()
    
    return filtered_desc

class AIProvider:
    """Classe base para provedores de IA."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def enhance_description(self, product: ProductInfo, config: Dict[str, Any] = None) -> str:
        """Método abstrato para melhorar descrição."""
        raise NotImplementedError
    
    def generate_seo_content(self, product: ProductInfo, config: Dict[str, Any] = None) -> SEOInfo:
        """Método abstrato para gerar conteúdo SEO."""
        raise NotImplementedError

class OpenAIProvider(AIProvider):
    """Provedor OpenAI GPT."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key)
        self.model = model
    
    def enhance_description(self, product: ProductInfo, config: Dict[str, Any] = None) -> str:
        """Melhora a descrição usando OpenAI GPT."""
        prompt = self._create_description_prompt(product, config)
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        attempts = 0
        delay = 1.0
        last_error = None
        while attempts < 3:
            try:
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "Você é um especialista em marketing de produtos. Sua tarefa é criar descrições de produtos detalhadas, atrativas e persuasivas que ajudem na conversão de vendas."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                return clean_markdown_formatting(response.choices[0].message.content.strip())
            except Exception as e:
                last_error = e
                attempts += 1
                logger.warning(f"Erro ao usar OpenAI (tentativa {attempts}/3): {str(e)}")
                time.sleep(delay)
                delay *= 2
        logger.error(f"Erro ao usar OpenAI após retries: {str(last_error)}")
        return product.description
    
    def generate_seo_content(self, product: ProductInfo, config: Dict[str, Any] = None) -> SEOInfo:
        """Gera Meta Title e Meta Description usando OpenAI GPT."""
        prompt = self._create_seo_prompt(product, config)
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        attempts = 0
        delay = 1.0
        last_error = None
        while attempts < 3:
            try:
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "Você é um especialista em SEO para e-commerce. Sua tarefa é criar Meta Title e Meta Description otimizados para produtos."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300,
                    temperature=0.7
                )
                content = clean_markdown_formatting(response.choices[0].message.content.strip())
                # Extrair Meta Title e Meta Description da resposta
                meta_title, meta_description = self._parse_seo_response(content, product)
                # Gerar descrição melhorada
                enhanced_description = self.enhance_description(product)
                return SEOInfo(
                    meta_title=meta_title,
                    meta_description=meta_description,
                    enhanced_description=enhanced_description
                )
            except Exception as e:
                last_error = e
                attempts += 1
                logger.warning(f"Erro ao gerar conteúdo SEO com OpenAI (tentativa {attempts}/3): {str(e)}")
                time.sleep(delay)
                delay *= 2
        logger.error(f"Erro ao gerar conteúdo SEO com OpenAI após retries: {str(last_error)}")
        # Fallback para valores padrão
        return SEOInfo(
            meta_title=self._generate_fallback_meta_title(product),
            meta_description=self._generate_fallback_meta_description(product),
            enhanced_description=product.description
        )

    def _create_description_prompt(self, product: ProductInfo, config: Dict[str, Any] = None) -> str:
        """Cria o prompt para melhorar descrição."""
        # Obter frases proibidas do config
        prohibited_phrases = (config or {}).get('prohibited_phrases', [])
        prohibited_text = ""
        if prohibited_phrases:
            prohibited_text = f"\n9. PROIBIDO: NÃO use as seguintes palavras/frases: {', '.join(prohibited_phrases)}"
        
        prompt = f"""
Crie uma descrição sucinta e atrativa para o seguinte produto, direcionada especificamente para donos de mercadinhos:

AUDIÊNCIA-ALVO:
Donos de mercadinhos (varejistas/lojistas) entre 35-54 anos, predominantemente masculinos. Valorizam preços baixos, entregas rápidas e condições de pagamento flexíveis. Possuem baixa literacia digital e gerenciam negócios familiares. Desempenham múltiplas funções: reposição, caixa e gestão geral.

PRODUTO:
Título: {product.title}
Descrição atual: {product.description}
Preço: {product.price or 'Não informado'}
SKU: {product.sku or 'Não informado'}
Categoria: {product.category or 'Não informada'}
Marca: {product.brand or 'Não informada'}

INSTRUÇÕES:
1. Use linguagem simples e direta, evitando termos técnicos complexos
2. Foque em benefícios práticos para o negócio (giro de estoque, aceitação dos clientes, facilidade de venda)
3. Destaque aspectos comerciais relevantes (prazo de validade, popularidade, qualidade)
4. Seja objetivo - máximo 2-3 frases
5. Use tom profissional mas acessível
6. Evite repetir o título
7. Foque em converter o varejista em comprador
8. IMPORTANTE: Retorne APENAS texto limpo, sem formatação Markdown (sem **, *, _, #, etc.){prohibited_text}

Descrição melhorada:"""
        return prompt
    
    def _create_seo_prompt(self, product: ProductInfo, config: Dict[str, Any] = None) -> str:
        """Cria o prompt para gerar conteúdo SEO seguindo as regras do Compra Agora."""
        # Usar título limpo para melhor geração de meta tags
        clean_title = clean_product_title(product.title)
        
        prompt = f"""
Crie Meta Title e Meta Description seguindo EXATAMENTE as regras do Compra Agora:

Título Original: {product.title}
Título Limpo: {clean_title}
Descrição: {product.description}
Preço: {product.price or 'Não informado'}
Categoria: {product.category or 'Não informada'}
Marca: {product.brand or 'Não informada'}

REGRAS OBRIGATÓRIAS DO COMPRA AGORA:

META TITLE:
• Usar a palavra-chave principal (nome do produto) no INÍCIO sempre que possível
• Manter entre 50 e 60 caracteres (para não cortar nos resultados)
• Ser claro e objetivo, mas chamativo
• Evitar repetições de palavras-chave (keyword stuffing)
• Incluir o nome da marca no final
• OBRIGATÓRIO: Terminar sempre com "- Compra Agora"
• Formato: "Nome Produto | Marca - Compra Agora"
• IMPORTANTE: Usar apenas o nome essencial do produto, sem especificações técnicas como volume, peso, cor, tamanho, etc.
• PREFERIR usar o "Título Limpo" fornecido acima

META DESCRIPTION:
• OBRIGATÓRIO: Entre 140 e 160 caracteres (acima disso o Google corta)
• Usar a palavra-chave principal de forma natural (não no início, não de forma engessada, seja o mais natural possível)
• Explicar de forma clara o que o usuário encontra na página
• Inserir gatilhos de ação ("Compre agora", "Descubra", "Veja modelos exclusivos")
• Destacar benefícios e diferenciais específicos do produto
• Incluir características técnicas relevantes quando aplicável
• Mencionar "Compra Agora" na descrição
• Ser persuasivo e atrativo para conversão
• Não duplicar descriptions em várias páginas
• IMPORTANTE: Focar no produto em si, não em especificações técnicas como volume ou embalagem
• CRÍTICO: Varie a estrutura - nem sempre comece com o nome do produto
• CRÍTICO: A palavra-chave deve fluir naturalmente no texto, como se fosse escrita por um humano
• CRÍTICO: Gere SEMPRE o texto COMPLETO dentro do limite de 160 caracteres - NUNCA corte no meio
• CRÍTICO: Planeje o texto para caber exatamente entre 140-160 caracteres, sem cortes
• CRÍTICO: Se o texto ficar muito longo, reescreva completamente para caber no limite
• CRÍTICO: NUNCA use reticências (...) ou corte palavras no meio
• CRÍTICO: O texto deve terminar sempre com call-to-action efetivo sem trocadilhos
• CRÍTICO: Use variações como "Adquira já!", "Confira ofertas!", "Veja mais!", "Descubra!"

PRESET DO NIARA:
META TITLE: tema/título + palavra-chave + audiência + tom de voz
META DESCRIPTION: tema/título + palavra-chave + audiência + call_to_action + tom de voz

EXEMPLOS DE META DESCRIPTION CONCISAS (140-160 caracteres):
- "Proteção invisível por 48h com fórmula avançada que combate o odor. Antitranspirante Dove Men+Care para sua confiança diária. Adquira já!" (155 caracteres)
- "Descubra o sabor rico de um blend premium para momentos especiais. Whisky Johnnie Walker Red Label com tradição escocesa. Adquira já!" (148 caracteres)
- "Fórmula avançada com proteção duradoura e frescor intenso. Antitranspirante Dove Men+Care para sua pele. Confira ofertas!" (134 caracteres - MUITO CURTO)

IMPORTANTE: Retorne APENAS texto limpo, sem formatação Markdown (sem **, *, _, #, etc.)

PROIBIDO: NÃO use as seguintes palavras/frases: {', '.join((config or {}).get('prohibited_phrases', []))}

Responda APENAS com:
META TITLE: [título aqui]
META DESCRIPTION: [descrição aqui]"""
        return prompt
    
    def _parse_seo_response(self, content: str, product: ProductInfo) -> Tuple[str, str]:
        """Extrai Meta Title e Meta Description da resposta da IA."""
        try:
            lines = content.split('\n')
            meta_title = ""
            meta_description = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith('META TITLE:'):
                    meta_title = clean_markdown_formatting(line.replace('META TITLE:', '').strip())
                elif line.startswith('META DESCRIPTION:'):
                    meta_description = clean_markdown_formatting(line.replace('META DESCRIPTION:', '').strip())
            
            # Validações e fallbacks
            if not meta_title or len(meta_title) > 60:
                meta_title = self._generate_fallback_meta_title(product)
            
            if not meta_description or len(meta_description) > 160:
                # NÃO CORTAR - usar fallback que gera texto completo
                logger.warning(f"Meta Description muito longa ({len(meta_description)} chars) - usando fallback")
                meta_description = self._generate_fallback_meta_description(product)
            
            return meta_title, meta_description
            
        except Exception as e:
            logger.error(f"Erro ao fazer parse da resposta SEO: {str(e)}")
            return (
                self._generate_fallback_meta_title(product),
                self._generate_fallback_meta_description(product)
            )
    
    def _generate_fallback_meta_title(self, product: ProductInfo) -> str:
        """Gera Meta Title padrão quando a IA falha."""
        title = product.title[:50]  # Limitar a 50 caracteres
        if product.brand and product.brand != 'Não informada':
            title = f"{title} | {product.brand}"
        if product.category and product.category != 'Não informada':
            title = f"{title} | {product.category}"
        return title[:60]  # Garantir máximo de 60
    
    def _generate_fallback_meta_description(self, product: ProductInfo) -> str:
        """Gera Meta Description padrão quando a IA falha."""
        # Usar título limpo para melhor resultado
        clean_title = clean_product_title(product.title)
        
        # Estrutura simples e concisa
        desc = f"Descubra {clean_title} com qualidade superior. Adquira já!"
        
        # Garantir que esteja entre 140-160 caracteres
        if len(desc) < 140:
            # Adicionar benefícios para atingir o mínimo
            benefits = self._get_benefits_by_category(clean_title, product.category)
            desc = f"Descubra {clean_title} com {benefits}. Adquira já!"
        
        # GARANTIR que sempre termine com call-to-action completo
        if not any(desc.endswith(cta) for cta in ["Adquira já!", "Confira ofertas!", "Veja mais!", "Descubra!"]):
            desc = f"{desc} Adquira já!"
        
        return desc[:160]

    def _get_benefits_by_category(self, clean_title: str, category: str) -> str:
        """Retorna benefícios baseados na categoria do produto."""
        if category and category != 'Não informada':
            if 'Smartphone' in clean_title or 'Celular' in clean_title:
                return "tecnologia avançada e recursos inovadores"
            elif 'Whisky' in clean_title or 'Bebida' in clean_title:
                return "sabor premium e qualidade excepcional"
            elif 'Antitranspirante' in clean_title or 'Desodorante' in clean_title:
                return "proteção duradoura e frescor intenso"
            elif 'TV' in clean_title or 'Televisão' in clean_title:
                return "imagem cristalina e som imersivo"
            elif 'Notebook' in clean_title or 'Laptop' in clean_title:
                return "performance excepcional e design moderno"
            else:
                return "qualidade superior e garantia de satisfação"
        else:
            return "qualidade superior e garantia de satisfação"

class GeminiProvider(AIProvider):
    """Provedor Google Gemini."""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        super().__init__(api_key)
        self.model = model
        genai.configure(api_key=api_key)
        self.model_instance = genai.GenerativeModel(model)
    
    def enhance_description(self, product: ProductInfo, config: Dict[str, Any] = None) -> str:
        """Melhora a descrição usando Google Gemini."""
        try:
            prompt = self._create_description_prompt(product, config)
            
            response = self.model_instance.generate_content(prompt)
            
            return clean_markdown_formatting(response.text.strip())
            
        except Exception as e:
            logger.error(f"Erro ao usar Gemini: {str(e)}")
            return product.description
    
    def generate_seo_content(self, product: ProductInfo, config: Dict[str, Any] = None) -> SEOInfo:
        """Gera Meta Title e Meta Description usando Google Gemini."""
        try:
            prompt = self._create_seo_prompt(product, config)
            
            response = self.model_instance.generate_content(prompt)
            content = clean_markdown_formatting(response.text.strip())
            
            # Extrair Meta Title e Meta Description da resposta
            meta_title, meta_description = self._parse_seo_response(content, product)
            
            # Gerar descrição melhorada
            enhanced_description = self.enhance_description(product)
            
            return SEOInfo(
                meta_title=meta_title,
                meta_description=meta_description,
                enhanced_description=enhanced_description
            )
            
        except Exception as e:
            logger.error(f"Erro ao gerar conteúdo SEO com Gemini: {str(e)}")
            # Fallback para valores padrão
            return SEOInfo(
                meta_title=self._generate_fallback_meta_title(product),
                meta_description=self._generate_fallback_meta_description(product),
                enhanced_description=product.description
            )

    def _create_description_prompt(self, product: ProductInfo, config: Dict[str, Any] = None) -> str:
        """Cria o prompt para melhorar descrição."""
        # Obter frases proibidas do config
        prohibited_phrases = (config or {}).get('prohibited_phrases', [])
        prohibited_text = ""
        if prohibited_phrases:
            prohibited_text = f"\n8. PROIBIDO: NÃO use as seguintes palavras/frases: {', '.join(prohibited_phrases)}"
        
        prompt = f"""
Crie uma descrição sucinta e atrativa para o seguinte produto:

Título: {product.title}
Descrição atual: {product.description}
Preço: {product.price or 'Não informado'}
SKU: {product.sku or 'Não informado'}
Categoria: {product.category or 'Não informada'}
Marca: {product.brand or 'Não informada'}

Instruções:
1. Seja direto e objetivo - máximo 2-3 frases
2. Destaque apenas os benefícios principais do produto
3. Use linguagem clara e persuasiva
4. Inclua informações práticas sobre uso/benefícios
5. Evite repetir o título
6. Foque em converter visitantes em compradores
7. IMPORTANTE: Retorne APENAS texto limpo, sem formatação Markdown (sem **, *, _, #, etc.){prohibited_text}

Descrição melhorada:"""
        return prompt
    
    def _create_seo_prompt(self, product: ProductInfo, config: Dict[str, Any] = None) -> str:
        """Cria o prompt para gerar conteúdo SEO seguindo as regras do Compra Agora."""
        # Usar título limpo para melhor geração de meta tags
        clean_title = clean_product_title(product.title)
        
        prompt = f"""
Crie Meta Title e Meta Description seguindo EXATAMENTE as regras do Compra Agora:

Título Original: {product.title}
Título Limpo: {clean_title}
Descrição: {product.description}
Preço: {product.price or 'Não informado'}
Categoria: {product.category or 'Não informada'}
Marca: {product.brand or 'Não informada'}

REGRAS OBRIGATÓRIAS DO COMPRA AGORA:

META TITLE:
• Usar a palavra-chave principal (nome do produto) no INÍCIO sempre que possível
• Manter entre 50 e 60 caracteres (para não cortar nos resultados)
• Ser claro e objetivo, mas chamativo
• Evitar repetições de palavras-chave (keyword stuffing)
• Incluir o nome da marca no final
• OBRIGATÓRIO: Terminar sempre com "- Compra Agora"
• Formato: "Nome Produto | Marca - Compra Agora"
• IMPORTANTE: Usar apenas o nome essencial do produto, sem especificações técnicas como volume, peso, cor, tamanho, etc.
• PREFERIR usar o "Título Limpo" fornecido acima

META DESCRIPTION:
• OBRIGATÓRIO: Entre 140 e 160 caracteres (acima disso o Google corta)
• Usar a palavra-chave principal de forma natural (não no início, não de forma engessada, seja o mais natural possível)
• Explicar de forma clara o que o usuário encontra na página
• Inserir gatilhos de ação ("Compre agora", "Descubra", "Veja modelos exclusivos")
• Destacar benefícios e diferenciais específicos do produto
• Incluir características técnicas relevantes quando aplicável
• Mencionar "Compra Agora" na descrição
• Ser persuasivo e atrativo para conversão
• Não duplicar descriptions em várias páginas
• IMPORTANTE: Focar no produto em si, não em especificações técnicas como volume ou embalagem
• CRÍTICO: Varie a estrutura - nem sempre comece com o nome do produto
• CRÍTICO: A palavra-chave deve fluir naturalmente no texto, como se fosse escrita por um humano
• CRÍTICO: Gere SEMPRE o texto COMPLETO dentro do limite de 160 caracteres - NUNCA corte no meio
• CRÍTICO: Planeje o texto para caber exatamente entre 140-160 caracteres, sem cortes
• CRÍTICO: Se o texto ficar muito longo, reescreva completamente para caber no limite
• CRÍTICO: NUNCA use reticências (...) ou corte palavras no meio
• CRÍTICO: O texto deve terminar sempre com call-to-action efetivo sem trocadilhos
• CRÍTICO: Use variações como "Adquira já!", "Confira ofertas!", "Veja mais!", "Descubra!"

PRESET DO NIARA:
META TITLE: tema/título + palavra-chave + audiência + tom de voz
META DESCRIPTION: tema/título + palavra-chave + audiência + call_to_action + tom de voz

EXEMPLOS DE META DESCRIPTION CONCISAS (140-160 caracteres):
- "Proteção invisível por 48h com fórmula avançada que combate o odor. Antitranspirante Dove Men+Care para sua confiança diária. Adquira já!" (155 caracteres)
- "Descubra o sabor rico de um blend premium para momentos especiais. Whisky Johnnie Walker Red Label com tradição escocesa. Adquira já!" (148 caracteres)
- "Fórmula avançada com proteção duradoura e frescor intenso. Antitranspirante Dove Men+Care para sua pele. Confira ofertas!" (134 caracteres - MUITO CURTO)

IMPORTANTE: Retorne APENAS texto limpo, sem formatação Markdown (sem **, *, _, #, etc.)

PROIBIDO: NÃO use as seguintes palavras/frases: {', '.join((config or {}).get('prohibited_phrases', []))}

Responda APENAS com:
META TITLE: [título aqui]
META DESCRIPTION: [descrição aqui]"""
        return prompt
    
    def _parse_seo_response(self, content: str, product: ProductInfo) -> Tuple[str, str]:
        """Extrai Meta Title e Meta Description da resposta da IA."""
        try:
            lines = content.split('\n')
            meta_title = ""
            meta_description = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith('META TITLE:'):
                    meta_title = clean_markdown_formatting(line.replace('META TITLE:', '').strip())
                elif line.startswith('META DESCRIPTION:'):
                    meta_description = clean_markdown_formatting(line.replace('META DESCRIPTION:', '').strip())
            
            # Validações e fallbacks
            if not meta_title or len(meta_title) > 60:
                meta_title = self._generate_fallback_meta_title(product)
            
            if not meta_description or len(meta_description) > 160:
                # NÃO CORTAR - usar fallback que gera texto completo
                logger.warning(f"Meta Description muito longa ({len(meta_description)} chars) - usando fallback")
                meta_description = self._generate_fallback_meta_description(product)
            
            return meta_title, meta_description
            
        except Exception as e:
            logger.error(f"Erro ao fazer parse da resposta SEO: {str(e)}")
            return (
                self._generate_fallback_meta_title(product),
                self._generate_fallback_meta_description(product)
            )
    
    def _generate_fallback_meta_title(self, product: ProductInfo) -> str:
        """Gera Meta Title padrão quando a IA falha."""
        title = product.title[:50]  # Limitar a 50 caracteres
        if product.brand and product.brand != 'Não informada':
            title = f"{title} | {product.brand}"
        if product.category and product.category != 'Não informada':
            title = f"{title} | {product.category}"
        return title[:60]  # Garantir máximo de 60
    
    def _generate_fallback_meta_description(self, product: ProductInfo) -> str:
        """Gera Meta Description padrão quando a IA falha."""
        # Usar título limpo para melhor resultado
        clean_title = clean_product_title(product.title)
        
        # Estrutura simples e concisa
        desc = f"Descubra {clean_title} com qualidade superior. Adquira já!"
        
        # Garantir que esteja entre 140-160 caracteres
        if len(desc) < 140:
            # Adicionar benefícios para atingir o mínimo
            benefits = self._get_benefits_by_category(clean_title, product.category)
            desc = f"Descubra {clean_title} com {benefits}. Adquira já!"
        
        # GARANTIR que sempre termine com call-to-action completo
        if not any(desc.endswith(cta) for cta in ["Adquira já!", "Confira ofertas!", "Veja mais!", "Descubra!"]):
            desc = f"{desc} Adquira já!"
        
        return desc[:160]

class ProductDescriptionEnhancer:
    """Classe principal para melhorar descrições de produtos."""
    
    def __init__(self, ai_provider: AIProvider, min_ratio: float = 1.5, config: Dict[str, Any] = None):
        self.ai_provider = ai_provider
        self.min_ratio = min_ratio
        self.config = config or load_config()
        self.prohibited_phrases = self.config.get('prohibited_phrases', [])
        self.stats = {
            'total_processed': 0,
            'enhanced': 0,
            'skipped': 0,
            'errors': 0
        }
    
    def should_enhance_description(self, title: str, description: str) -> Tuple[bool, str]:
        """
        Verifica se a descrição deve ser melhorada.
        
        Args:
            title: Título do produto
            description: Descrição atual do produto
            
        Returns:
            Tuple (deve_melhorar, motivo)
        """
        # SEMPRE MELHORAR - Deixar a IA decidir se vale a pena ou não
        return True, "Sempre melhorar com base no retorno da IA"
    
    def create_product_info(self, row: pd.Series, column_mapping: Dict[str, str]) -> ProductInfo:
        """
        Cria objeto ProductInfo a partir de uma linha do DataFrame.
        
        Args:
            row: Linha do DataFrame
            column_mapping: Mapeamento de colunas
            
        Returns:
            ProductInfo com dados do produto
        """
        return ProductInfo(
            title=str(row.get(column_mapping.get('title', 'title'), '')).strip(),
            description=str(row.get(column_mapping.get('description', 'description'), '')).strip(),
            price=str(row.get(column_mapping.get('price', 'price'), '')).strip(),
            sku=str(row.get(column_mapping.get('sku', 'sku'), '')).strip(),
            category=str(row.get(column_mapping.get('category', 'category'), '')).strip(),
            brand=str(row.get(column_mapping.get('brand', 'brand'), '')).strip()
        )
    
    def _is_too_similar(self, enhanced: str, original: str, threshold: float = 0.8) -> bool:
        """
        Verifica se a descrição melhorada é muito similar à original.
        
        Args:
            enhanced: Descrição melhorada
            original: Descrição original
            threshold: Limite de similaridade (0.8 = 80%)
            
        Returns:
            True se for muito similar
        """
        if not enhanced or not original:
            return False
        
        # Normalizar textos para comparação
        enhanced_clean = re.sub(r'[^\w\s]', '', enhanced.lower()).strip()
        original_clean = re.sub(r'[^\w\s]', '', original.lower()).strip()
        
        # Usar difflib para calcular similaridade
        similarity = difflib.SequenceMatcher(None, enhanced_clean, original_clean).ratio()
        
        return similarity >= threshold
    
    def _generate_rule_based_description(self, product: ProductInfo) -> str:
        """
        Gera descrição baseada em regras quando a IA falha ou é muito similar.
        
        Args:
            product: Informações do produto
            
        Returns:
            Descrição gerada por regras
        """
        title = product.title
        original_desc = product.description
        
        # Templates baseados em categoria/tipo de produto
        if any(word in title.lower() for word in ['smartphone', 'celular', 'telefone']):
            template = f"{title} oferece tecnologia avançada com recursos inovadores para sua comunicação diária. Ideal para quem busca performance e qualidade em um dispositivo moderno e confiável."
        elif any(word in title.lower() for word in ['whisky', 'bebida', 'drink']):
            template = f"Desfrute do sabor premium de {title} com qualidade excepcional. Perfeito para momentos especiais, oferecendo uma experiência única de degustação."
        elif any(word in title.lower() for word in ['antitranspirante', 'desodorante']):
            template = f"{title} proporciona proteção duradoura e frescor intenso por até 24 horas. Fórmula desenvolvida para manter você confiante durante todo o dia."
        elif any(word in title.lower() for word in ['tv', 'televisão', 'televisor']):
            template = f"Experimente imagem cristalina e som imersivo com {title}. Tecnologia de ponta para entretenimento de qualidade superior em sua casa."
        elif any(word in title.lower() for word in ['notebook', 'laptop', 'computador']):
            template = f"{title} combina performance excepcional com design moderno. Ideal para trabalho e entretenimento com eficiência e confiabilidade."
        else:
            # Template genérico
            template = f"{title} oferece qualidade superior e garantia de satisfação. Produto desenvolvido com tecnologia avançada para atender suas necessidades com excelência."
        
        # Se tiver descrição original, tentar incorporar elementos únicos
        if original_desc and len(original_desc.strip()) > 10:
            # Extrair palavras-chave únicas da descrição original
            original_words = set(original_desc.lower().split())
            common_words = {'o', 'a', 'os', 'as', 'de', 'da', 'do', 'das', 'dos', 'em', 'na', 'no', 'com', 'para', 'por', 'que', 'e', 'ou', 'se', 'é', 'são'}
            unique_words = [word for word in original_words if word not in common_words and len(word) > 3]
            
            if unique_words:
                # Adicionar algumas palavras-chave únicas ao template
                keywords = ', '.join(unique_words[:3])
                template += f" Características especiais incluem {keywords} para melhor desempenho."
        
        return template
    
    def process_excel_file(self, input_file: str, output_file: str = None, 
                          column_mapping: Dict[str, str] = None) -> None:
        """
        Processa arquivo Excel com catálogo de produtos.
        
        Args:
            input_file: Caminho do arquivo Excel de entrada
            output_file: Caminho do arquivo Excel de saída
            column_mapping: Mapeamento personalizado de colunas
        """
        try:
            # Mapeamento padrão de colunas
            default_mapping = {
                'title': 'Título',
                'description': 'Descrição', 
                'price': 'Preço',
                'sku': 'SKU',
                'category': 'Categoria',
                'brand': 'Marca'
            }
            
            if column_mapping:
                default_mapping.update(column_mapping)
            
            # Ler planilha
            logger.info(f"Lendo arquivo: {input_file}")
            df = pd.read_excel(input_file)
            
            # Verificar colunas necessárias
            required_columns = [default_mapping['title'], default_mapping['description']]
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"Colunas necessárias não encontradas: {missing_columns}")
            
            # Adicionar colunas de resultado
            df['Descrição_Melhorada'] = ''
            df['Status_Melhoria'] = ''
            df['Motivo_Melhoria'] = ''
            df['Razão_Título_Descrição'] = ''
            df['Meta_Title'] = ''  # Nova coluna para Meta Title
            df['Meta_Description'] = ''  # Nova coluna para Meta Description
            
            # Processar cada linha
            total_rows = len(df)
            logger.info(f"Processando {total_rows} produtos...")
            
            for index, row in df.iterrows():
                try:
                    # Criar objeto do produto
                    product = self.create_product_info(row, default_mapping)
                    
                    # Limpar título para melhorar a geração de meta tags
                    product.title = clean_product_title(product.title)
                    
                    # Calcular razão título/descrição
                    title_length = len(product.title)
                    description_length = len(product.description)
                    ratio = description_length / title_length if title_length > 0 else 0
                    
                    df.at[index, 'Razão_Título_Descrição'] = f"{ratio:.2f}"
                    
                    # Verificar se deve melhorar
                    should_enhance, motivo = self.should_enhance_description(product.title, product.description)
                    df.at[index, 'Motivo_Melhoria'] = motivo
                    
                    if should_enhance:
                        logger.info(f"Melhorando produto {index + 1}/{total_rows}: {product.title[:50]}... (Motivo: {motivo})")
                        logger.info(f"  Descrição ATUAL: {product.description}")
                        
                        # Gerar conteúdo SEO completo (descrição + meta tags)
                        seo_info = self.ai_provider.generate_seo_content(product, self.config)
                        
                        # Verificar similaridade e tentar retries se necessário
                        enhanced = seo_info.enhanced_description or ""
                        if self._is_too_similar(enhanced, product.description):
                            logger.warning("  Descrição melhorada muito similar à original. Tentando nova geração...")
                            max_retries = 2
                            for attempt in range(1, max_retries + 1):
                                time.sleep(0.5)
                                candidate = self.ai_provider.enhance_description(product, self.config) or ""
                                if not self._is_too_similar(candidate, product.description):
                                    enhanced = candidate
                                    logger.info(f"  Nova variação aceita na tentativa {attempt}")
                                    break
                            else:
                                # Fallback baseado em regras para garantir mudança
                                logger.warning("  Mantida alta similaridade após retries. Aplicando fallback baseado em regras.")
                                enhanced = self._generate_rule_based_description(product)
                        
                        # Filtrar conteúdo proibido (apenas como medida de segurança mínima)
                        # A IA já foi instruída a não usar essas palavras nos prompts
                        enhanced = filter_prohibited_content(enhanced, self.prohibited_phrases)
                        
                        # Validar comprimento da descrição
                        enhanced = ensure_description_length(enhanced)
                        
                        # Atualizar DataFrame com todas as informações
                        df.at[index, 'Descrição_Melhorada'] = enhanced
                        df.at[index, 'Meta_Title'] = seo_info.meta_title
                        df.at[index, 'Meta_Description'] = seo_info.meta_description
                        df.at[index, 'Status_Melhoria'] = 'MELHORADO'
                        
                        # Log das informações geradas
                        logger.info(f"  Descrição MELHORADA: {enhanced}")
                        logger.info(f"  Meta Title: {seo_info.meta_title}")
                        logger.info(f"  Meta Description: {seo_info.meta_description}")
                        logger.info(f"  Tamanho: {len(product.description)} → {len(enhanced)} caracteres")
                        
                        self.stats['enhanced'] += 1
                        
                        # Pausa para não sobrecarregar APIs
                        time.sleep(1)
                        
                    else:
                        # Mesmo sem melhorar, gerar meta tags para todos os produtos
                        logger.info(f"  MANTIDO: {product.title[:50]}... (Motivo: {motivo})")
                        logger.info(f"  Gerando meta tags para produto mantido...")
                        
                        # Gerar apenas meta tags (sem melhorar descrição)
                        seo_info = self.ai_provider.generate_seo_content(product, self.config)
                        
                        df.at[index, 'Descrição_Melhorada'] = product.description
                        df.at[index, 'Meta_Title'] = seo_info.meta_title
                        df.at[index, 'Meta_Description'] = seo_info.meta_description
                        df.at[index, 'Status_Melhoria'] = 'MANTIDO'
                        
                        self.stats['skipped'] += 1
                        
                        # Pausa menor para produtos mantidos
                        time.sleep(0.5)
                    
                    self.stats['total_processed'] += 1
                    
                    # Log de progresso a cada 10 produtos
                    if (index + 1) % 10 == 0:
                        logger.info(f"Progresso: {index + 1}/{total_rows} produtos processados")
                
                except Exception as e:
                    logger.error(f"Erro ao processar linha {index + 1}: {str(e)}")
                    df.at[index, 'Status_Melhoria'] = 'ERRO'
                    df.at[index, 'Descrição_Melhorada'] = product.description if 'product' in locals() else ''
                    df.at[index, 'Meta_Title'] = ''
                    df.at[index, 'Meta_Description'] = ''
                    self.stats['errors'] += 1
            
            # Salvar resultado
            if not output_file:
                if input_file.endswith('.xlsx'):
                    output_file = input_file.replace('.xlsx', '_melhorado.xlsx')
                elif input_file.endswith('.xls'):
                    output_file = input_file.replace('.xls', '_melhorado.xlsx')
                else:
                    output_file = input_file + '_melhorado.xlsx'
            
            df.to_excel(output_file, index=False, engine='openpyxl')
            
            # Estatísticas finais
            logger.info(f"Processamento concluído!")
            logger.info(f"Total processado: {self.stats['total_processed']}")
            logger.info(f"Melhorados: {self.stats['enhanced']}")
            logger.info(f"Mantidos: {self.stats['skipped']}")
            logger.info(f"Erros: {self.stats['errors']}")
            logger.info(f"Arquivo salvo: {output_file}")
            logger.info(f" Meta Title e Meta Description gerados para todos os produtos!")
            
        except Exception as e:
            logger.error(f"Erro ao processar arquivo: {str(e)}")
            raise

def get_dynamic_length_limits(original_description: str, config: Dict[str, Any]) -> Tuple[int, int]:
    """
    Calcula limites de comprimento dinâmicos baseados na descrição original.
    
    Args:
        original_description: Descrição original do produto
        config: Configuração de comprimento
        
    Returns:
        Tuple (min_chars, max_chars)
    """
    original_length = len(original_description.strip())
    
    # Verificar se usar regras dinâmicas
    if not config.get("dynamic_rules", False):
        return config.get("min_chars", 300), config.get("max_chars", 450)
    
    threshold = config.get("short_description", {}).get("threshold", 300)
    
    if original_length < threshold:
        # Descrição original curta: 300-400 caracteres
        short_config = config.get("short_description", {})
        return short_config.get("min_chars", 300), short_config.get("max_chars", 400)
    else:
        # Descrição original longa: 300-800 caracteres  
        long_config = config.get("long_description", {})
        return long_config.get("min_chars", 300), long_config.get("max_chars", 800)

def ensure_description_length(description: str, min_chars: int = 300, max_chars: int = 450) -> str:
    """
    Garante que a descrição tenha entre min_chars e max_chars caracteres.
    
    Args:
        description: Descrição a ser validada
        min_chars: Mínimo de caracteres
        max_chars: Máximo de caracteres
        
    Returns:
        Descrição ajustada
    """
    if not description:
        return description
    
    current_length = len(description)
    
    # Se está muito curta, expandir
    if current_length < min_chars:
        # Adicionar frases complementares
        expansions = [
            " Este produto oferece excelente qualidade e durabilidade.",
            " Ideal para uso diário com máxima eficiência.",
            " Desenvolvido com tecnologia avançada para melhor desempenho.",
            " Garante satisfação e resultados superiores.",
            " Produto confiável com ótima aceitação no mercado."
        ]
        
        for expansion in expansions:
            if len(description + expansion) <= max_chars:
                description += expansion
                if len(description) >= min_chars:
                    break
    
    # Se está muito longa, cortar preservando frases completas
    elif current_length > max_chars:
        # Encontrar último ponto antes do limite
        truncated = description[:max_chars]
        last_period = truncated.rfind('.')
        if last_period > min_chars:
            description = truncated[:last_period + 1]
        else:
            description = truncated[:max_chars].rstrip() + "."
    
    return description

def load_config() -> Dict[str, Any]:
    """Carrega configuração do arquivo config.json."""
    config_file = Path('config.json')
    
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return {}

def main():
    """Função principal do script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Melhorador de descrições de produtos usando IA com geração de Meta Title e Meta Description')
    parser.add_argument('input_file', help='Arquivo Excel com catálogo de produtos')
    parser.add_argument('-o', '--output', help='Arquivo Excel de saída (opcional)')
    parser.add_argument('-p', '--provider', choices=['openai', 'gemini'], default='openai', 
                       help='Provedor de IA (padrão: openai)')
    parser.add_argument('-k', '--api-key', help='Chave da API (ou use variável de ambiente)')
    parser.add_argument('-r', '--ratio', type=float, default=1.5, 
                       help='Razão mínima descrição/título para melhorar (padrão: 1.5)')
    parser.add_argument('-m', '--model', help='Modelo específico (ex: gpt-4, gemini-pro)')
    
    args = parser.parse_args()
    
    # Carregar configuração
    config = load_config()
    
    # Determinar chave da API
    api_key = args.api_key or os.getenv('OPENAI_API_KEY') if args.provider == 'openai' else os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        raise ValueError(f"Chave da API {args.provider.upper()}_API_KEY não encontrada. Configure via argumento -k ou variável de ambiente.")
    
    # Criar provedor de IA
    if args.provider == 'openai':
        model = args.model or config.get('openai_model', 'gpt-3.5-turbo')
        ai_provider = OpenAIProvider(api_key, model)
    else:  # gemini
        model = args.model or config.get('gemini_model', 'gemini-pro')
        ai_provider = GeminiProvider(api_key, model)
    
    # Criar melhorador
    enhancer = ProductDescriptionEnhancer(ai_provider, args.ratio, config)
    
    # Processar arquivo
    enhancer.process_excel_file(args.input_file, args.output)

if __name__ == "__main__":
    main() 