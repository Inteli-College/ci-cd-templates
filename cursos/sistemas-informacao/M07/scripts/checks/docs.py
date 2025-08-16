from shared.utils.file_checks import file_exists

def run_all():
    """
    Verifica se os documentos obrigatórios existem.
    """
    results = []
    obrigatorios = [
        "docs/planejamento.md",
        "docs/relatorio.md"
    ]
    for doc in obrigatorios:
        status = "ok" if file_exists(doc) else "fail"
        results.append({"check": f"Documento {doc}", "status": status})
    return results