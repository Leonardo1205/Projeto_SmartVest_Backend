from pathlib import Path
import argparse
import shutil

from app.services.ingest_topic import (
    build_index,
    DATA_DIR,   
    INDEX_DIR,  
)

def list_slugs() -> list[str]:
    """Lista todos os slugs existentes em app/data/topics/*"""
    if not DATA_DIR.exists():
        return []
    return sorted([p.name for p in DATA_DIR.iterdir() if p.is_dir()])

def ingest_many(only: list[str] | None = None, rebuild: bool = False) -> None:
    slugs = list_slugs()
    if only:
        wanted = set(only)
        slugs = [s for s in slugs if s in wanted]

    if not slugs:
        print("Nenhum tópico encontrado em", DATA_DIR)
        return

    print(f"➡️  Iniciando ingest de {len(slugs)} tópico(s)...\n")

    for slug in slugs:
        try:
            if rebuild:
                shutil.rmtree(INDEX_DIR / slug, ignore_errors=True)
            print(f"→ {slug}")
            build_index(slug)
        except Exception as e:
            print(f"❌  Falha em {slug}: {e}")
        else:
            print(f"✅  {slug} finalizado\n")

    print("🏁  Processo concluído.")

def main():
    parser = argparse.ArgumentParser(
        description="Ingesta em lote dos tópicos (gera/atualiza os índices FAISS)."
    )
    parser.add_argument(
        "--only",
        nargs="*",
        help="Lista de slugs específicos (se omitido, roda para todos). Ex.: --only renda-fixa-vs-variavel liquidez",
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Apaga o índice do tópico antes de recriar.",
    )
    args = parser.parse_args()
    ingest_many(only=args.only, rebuild=args.rebuild)

if __name__ == "__main__":
    main()
