from shared.utils.file_checks import dir_exists

def run_all():
    """
    Garante que a pasta 'assets' existe e contém pelo menos 1 arquivo.
    """
    pasta = "assets"
    if not dir_exists(pasta):
        return [{"check": "Pasta assets presente", "status": "fail"}]

    import os
    arquivos = [f for f in os.listdir(pasta) if not f.startswith(".")]
    status = "ok" if arquivos else "fail"
    return [{"check": "Pasta assets com arquivos", "status": status}]