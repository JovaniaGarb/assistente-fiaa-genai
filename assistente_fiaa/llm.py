"""Provedores de geração. A rota e a segurança são decididas antes (guardrails/policy)."""
from __future__ import annotations

import json
import os
import re
from typing import Protocol

from . import config


class Provider(Protocol):
    name: str
    def complete(self, system: str, user: str) -> str: ...


class AnthropicProvider:
    """LLM real via API da Anthropic. Requer ANTHROPIC_API_KEY. Não foi executado no ambiente de
    desenvolvimento deste repositório (sem chave); ver README, seção 'Rodando com LLM'."""
    name = "anthropic"

    def __init__(self, model: str | None = None):
        import anthropic  # import tardio: dependência opcional
        self.model = model or config.MODEL
        self.client = anthropic.Anthropic()

    def complete(self, system: str, user: str) -> str:
        kwargs = dict(model=self.model, max_tokens=config.MAX_TOKENS, system=system,
                      messages=[{"role": "user", "content": user}])
        temp = os.getenv("LLM_TEMPERATURE")
        if temp:
            kwargs["temperature"] = float(temp)
        msg = self.client.messages.create(**kwargs)
        return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")


class OpenAICompatProvider:
    """LLM por qualquer endpoint compatível com a API 'chat/completions' (Ollama local, Groq, OpenRouter,
    Gemini em modo compatível, etc.). Só biblioteca padrão. Configuração por variáveis de ambiente:
      LLM_BASE_URL  (padrão http://localhost:11434/v1 = Ollama)   LLM_MODEL (padrão llama3.1:8b)
      LLM_API_KEY   (qualquer texto para Ollama)                  LLM_JSON_MODE=1 (pede saída JSON, se suportado)"""
    name = "openai-compat"

    def __init__(self):
        self.base = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1").rstrip("/")
        self.model = os.getenv("LLM_MODEL", "llama3.1:8b")
        self.key = os.getenv("LLM_API_KEY", "ollama")
        self.json_mode = os.getenv("LLM_JSON_MODE", "") == "1"
        self.timeout = int(os.getenv("LLM_TIMEOUT", "180"))
        # Gemini (modo compatível) aceita response_format=json_object: liga sozinho; nos demais, LLM_JSON_MODE=1
        if "generativelanguage.googleapis.com" in self.base and os.getenv("LLM_JSON_MODE") is None:
            self.json_mode = True
        self.reasoning = os.getenv("LLM_REASONING_EFFORT", "")   # opcional: low|medium|high|none (se o servidor aceitar)
        self.ultimo_finish = ""   # finish_reason da última chamada (ex.: 'length' = resposta cortada)

    def complete(self, system: str, user: str) -> str:
        import urllib.request
        corpo = {"model": self.model, "temperature": float(os.getenv("LLM_TEMPERATURE", "0")),
                 "max_tokens": config.MAX_TOKENS,
                 "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
        if self.json_mode:
            corpo["response_format"] = {"type": "json_object"}
        if self.reasoning:
            corpo["reasoning_effort"] = self.reasoning
        req = urllib.request.Request(self.base + "/chat/completions", json.dumps(corpo).encode("utf-8"),
                                     {"Content-Type": "application/json", "Authorization": f"Bearer {self.key}"})
        import time
        import urllib.error
        espera = float(os.getenv("LLM_RETRY_WAIT", "15"))
        for tentativa in range(4):   # limites de camadas gratuitas devolvem 429: espera e tenta de novo
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    dados = json.load(r)
                break
            except urllib.error.HTTPError as e:
                if e.code in (429, 503) and tentativa < 3:
                    time.sleep(espera * (tentativa + 1))
                    continue
                raise
        escolha = dados["choices"][0]
        self.ultimo_finish = str(escolha.get("finish_reason") or "")
        return escolha["message"].get("content") or ""


class ScriptedProvider:
    """Provedor para testes: devolve respostas pré-definidas (inclusive respostas ruins)."""
    name = "scripted"

    def __init__(self, respostas: list[str]):
        self.respostas = list(respostas)
        self.chamadas: list[tuple[str, str]] = []

    def complete(self, system: str, user: str) -> str:
        self.chamadas.append((system, user))
        return self.respostas.pop(0) if self.respostas else "{}"


def parse_json(txt: str) -> dict | None:
    """Extrai o primeiro objeto JSON do texto, tolerando cercas de código."""
    txt = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
    try:
        return json.loads(txt)
    except Exception:
        m = re.search(r"\{.*\}", txt, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return None
    return None


def build_provider(nome: str | None = None) -> Provider | None:
    nome = nome or config.PROVIDER
    if nome == "anthropic":
        return AnthropicProvider()
    if nome in ("openai", "ollama", "openai-compat"):
        return OpenAICompatProvider()
    return None   # "extractive": sem LLM
