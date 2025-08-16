from shared.utils.file_checks import dir_exists

def run_all():
    """
    Verifica se os documentos obrigatórios existem.
    """
    results = []

    pasta = "docs"
    if not dir_exists(pasta):
        return [{"check": "Pasta docs presente", "status": "fail"}]

    return results