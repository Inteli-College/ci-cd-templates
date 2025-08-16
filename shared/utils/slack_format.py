def format_message(results):
    success = sum(1 for r in results if r["status"] == "ok")
    total = len(results)
    return {
        "text": f"Avaliação concluída: {success}/{total} critérios OK",
        "attachments": [
            {"title": "Detalhes",
             "text": "\n".join([f"{r['check']}: {r['status']}" for r in results])}
        ]
    }