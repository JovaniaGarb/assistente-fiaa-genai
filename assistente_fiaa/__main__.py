"""CLI: python -m assistente_fiaa  (web | demo | chamado "texto" | interativo | fila | avaliar)."""
from __future__ import annotations

import argparse
import json
import sys

from . import config
from .llm import build_provider
from .pipeline import Assistente


def _assistente(args) -> Assistente:
    try:
        prov = build_provider(args.provider)
    except ImportError:
        sys.exit("Modo anthropic requer: pip install anthropic  (e a variável ANTHROPIC_API_KEY).")
    except Exception as e:  # ex.: chave ausente
        sys.exit(f"Não foi possível iniciar o provedor '{args.provider}': {e}")
    return Assistente(provider=prov)


def cmd_chamado(args):
    r = _assistente(args).processar(" ".join(args.texto), "CLI-1")
    print(json.dumps(r.to_dict(), ensure_ascii=False, indent=2) if args.json else r.to_markdown())


def cmd_demo(args):
    a = _assistente(args)
    dados = json.loads((config.TICKETS_DIR / "chamados.json").read_text(encoding="utf-8"))["chamados"]
    for c in dados:
        print(f"\n{'=' * 78}\n{c['id']} [{c['categoria']}] {c['titulo']}\nCHAMADO: {c['texto']}\n")
        print(a.processar(c["texto"], c["id"]).to_markdown())
        if "rodada_2" in c:
            print(f"\n--- Rodada 2 (usuário responde): {c['rodada_2']['resposta_usuario']}\n")
            print(a.processar(c["rodada_2"]["resposta_usuario"], c["id"]).to_markdown())


def cmd_interativo(args):
    a = _assistente(args)
    print("Assistente FI-AA (protótipo). Digite o chamado; linha vazia sai. Ctrl+C também sai.")
    while True:
        try:
            t = input("\nchamado> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not t:
            break
        print("\n" + a.processar(t, "INTERATIVO").to_markdown())


def cmd_fila(args):
    a = Assistente()
    if args.decidir:
        item = a.fila.decidir(args.decidir, args.aprovar, args.revisor, args.comentario)
        print(json.dumps(item, ensure_ascii=False, indent=2))
        a.audit.registrar({"evento": "decisao_humana", "hitl_id": item["id"], "ticket_id": item["ticket_id"],
                           "status": item["status"], "revisor": args.revisor})
        return
    for i in a.fila.listar(args.status):
        print(f"{i['id']} {i['ticket_id']:8} {i['status']:9} {i['rota']:22} {i['motivo']}")


def cmd_web(args):
    from .web import servir
    try:
        prov = build_provider(args.provider)
    except Exception as e:
        sys.exit(f"Não foi possível iniciar o provedor '{args.provider}': {e}")
    servir(prov, args.porta, not args.sem_navegador)


def cmd_avaliar(args):
    from .avaliacao import executar
    sys.exit(0 if executar(args.provider) else 1)


def main():
    ap = argparse.ArgumentParser(prog="assistente_fiaa")
    ap.add_argument("--provider", default=None, help="extractive (padrão, offline) | anthropic (LLM, requer ANTHROPIC_API_KEY)")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("chamado"); p.add_argument("texto", nargs="+"); p.add_argument("--json", action="store_true"); p.set_defaults(f=cmd_chamado)
    sp.add_parser("demo").set_defaults(f=cmd_demo)
    sp.add_parser("interativo").set_defaults(f=cmd_interativo)
    p = sp.add_parser("fila"); p.add_argument("--status"); p.add_argument("--decidir"); p.add_argument("--aprovar", action="store_true")
    p.add_argument("--revisor", default="consultor.humano"); p.add_argument("--comentario", default=""); p.set_defaults(f=cmd_fila)
    p = sp.add_parser("web"); p.add_argument("--porta", type=int, default=8765); p.add_argument("--sem-navegador", action="store_true"); p.set_defaults(f=cmd_web)
    sp.add_parser("avaliar").set_defaults(f=cmd_avaliar)
    args = ap.parse_args()
    args.f(args)


if __name__ == "__main__":
    main()
