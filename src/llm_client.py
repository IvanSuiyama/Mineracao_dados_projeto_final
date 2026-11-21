"""
Cliente para a API do DeepSeek (compatível com o SDK da OpenAI).

Uso:
    from src.llm_client import interpretar_resultados
    texto = interpretar_resultados(resumo_json, pergunta)

A chave é lida do arquivo .env (variavel DEEPSEEK_API_KEY).
NUNCA coloque a chave direto no codigo nem no notebook.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Carrega o .env que estiver na raiz do projeto
RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")

BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
MODELO = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")


PROMPT_SISTEMA = """Você é um analista de dados auxiliando na interpretação de resultados
de Mineração de Dados. Regras obrigatórias:
1. Use SOMENTE os números e informações fornecidos no resumo.
2. NÃO invente valores, jogos, grupos ou estatísticas que não estejam no resumo.
3. Se algo não estiver no resumo, diga explicitamente que não foi fornecido.
4. Escreva em português do Brasil, de forma clara e objetiva.
5. Estruture a resposta em: (a) padrões principais, (b) perfis/grupos encontrados,
   (c) jogos mais semelhantes e mais atípicos, (d) conclusão curta.
6. Não afirme causalidade; descreva associações observadas."""


def _cliente() -> OpenAI:
    chave = os.getenv("DEEPSEEK_API_KEY")
    if not chave:
        raise RuntimeError(
            "DEEPSEEK_API_KEY não encontrada. Crie um arquivo .env na raiz "
            "do projeto (copie de .env.example) e preencha a chave."
        )
    return OpenAI(api_key=chave, base_url=BASE_URL)


def interpretar_resultados(
    resumo: dict | str,
    pergunta: str,
    modelo: str = MODELO,
    temperatura: float = 0.2,
) -> str:
    """Envia o resumo agregado para a LLM e retorna a interpretação em texto."""
    if isinstance(resumo, dict):
        resumo_txt = json.dumps(resumo, ensure_ascii=False, indent=2)
    else:
        resumo_txt = str(resumo)

    mensagem_usuario = (
        f"Pergunta principal da análise:\n{pergunta}\n\n"
        f"Resumo produzido pelo código Python (fonte única de verdade):\n"
        f"{resumo_txt}\n\n"
        "Interprete os resultados seguindo as regras."
    )

    resposta = _cliente().chat.completions.create(
        model=modelo,
        temperature=temperatura,
        messages=[
            {"role": "system", "content": PROMPT_SISTEMA},
            {"role": "user", "content": mensagem_usuario},
        ],
    )
    return resposta.choices[0].message.content


def registrar_interacao(prompt_sistema: str, prompt_usuario: str, resposta: str,
                        destino: str | Path) -> None:
    """Salva prompt + resposta para o relatorio (comprova a integracao)."""
    destino = Path(destino)
    destino.write_text(
        json.dumps(
            {
                "modelo": MODELO,
                "prompt_sistema": prompt_sistema,
                "prompt_usuario": prompt_usuario,
                "resposta": resposta,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
