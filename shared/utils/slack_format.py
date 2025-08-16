def format_message(results):
    """Formata mensagem para o Slack baseado no formato dos resultados"""
    
    # Verifica se é o formato novo (com summary, status, details)
    if isinstance(results, dict) and 'summary' in results:
        status_emoji = "✅" if results.get('status') == 'success' else "❌"
        success_rate = results.get('success_rate', 0)
        
        return {
            "text": f"{status_emoji} Validação Automatizada Concluída",
            "attachments": [
                {
                    "title": "Resumo da Validação",
                    "text": f"{results.get('summary', 'Sem resumo')}\n📈 Taxa de Sucesso: {success_rate:.1f}%",
                    "color": "good" if results.get('status') == 'success' else "danger"
                }
            ]
        }
    
    # Formato antigo (lista de resultados)
    elif isinstance(results, list):
        success = sum(1 for r in results if r.get("status") == "ok")
        total = len(results)
        success_rate = (success / total) * 100 if total > 0 else 0
        
        return {
            "text": f"Avaliação concluída: {success}/{total} critérios OK ({success_rate:.1f}%)",
            "attachments": [
                {
                    "title": "Detalhes",
                    "text": "\n".join([f"{r.get('check', 'Unknown')}: {r.get('status', 'Unknown')}" for r in results])
                }
            ]
        }
    
    # Fallback para formato desconhecido
    else:
        return {
            "text": "📊 Validação executada",
            "attachments": [
                {
                    "title": "Resultado",
                    "text": str(results) if results else "Nenhum resultado disponível"
                }
            ]
        }