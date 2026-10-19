"""Configuração central. Valores podem ser sobrescritos por variáveis de ambiente."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KB_DIR = Path(os.getenv("KB_DIR", ROOT / "knowledge_base"))
TICKETS_DIR = ROOT / "tickets"
LOG_DIR = Path(os.getenv("LOG_DIR", ROOT / "logs"))
EVIDENCE_DIR = ROOT / "evidencias"

# Provedor de geração: "extractive" (offline, sem LLM) ou "anthropic" (LLM)
PROVIDER = os.getenv("PROVIDER", "extractive")
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5")
# Modelos com "raciocínio" (ex.: Gemini 2.5/3) gastam parte do limite pensando; 1500 truncava o JSON. Ajuste com LLM_MAX_TOKENS.
MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "6000"))

# Recuperação e confiança (calibrados em tests/ e evidencias/; ver README)
TOP_K = int(os.getenv("TOP_K", "6"))
LIMIAR_RELEVANCIA = float(os.getenv("LIMIAR_RELEVANCIA", "0.20"))   # abaixo: sem evidência
LIMIAR_ALTO = float(os.getenv("LIMIAR_ALTO", "0.40"))               # acima: trecho forte
MAX_RODADAS_PERGUNTAS = 2                                            # KB-FIAA-011
MAX_PERGUNTAS_POR_RODADA = 5                                         # KB-FIAA-011

PROMPT_VERSION = "v1.0"
