from shared.utils.file_checks import dir_exists

def run_all():
    """
    Verifica se a pasta 'src' existe e contém pelo menos um arquivo .py.
    """
    pasta = "src"
    if not dir_exists(pasta):
        return [{"check": "Pasta src presente", "status": "fail"}]

    import os
    arquivos_py = [f for f in os.listdir(pasta) if f.endswith(".py")]
    status = "ok" if arquivos_py else "fail"
    return [{"check": "Arquivos Python na pasta src", "status": status}]