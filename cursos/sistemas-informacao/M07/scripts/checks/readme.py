from shared.utils.file_checks import file_exists

def run_all():
    """
    Confere se README.md existe e não está vazio.
    """
    path = "README.md"
    if not file_exists(path):
        return [{"check": "README.md presente", "status": "fail"}]

    with open(path, encoding="utf-8") as f:
        content = f.read().strip()
    status = "ok" if content else "fail"
    return [{"check": "README.md não vazio", "status": status}]