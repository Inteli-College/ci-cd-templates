# Funções de formatação
def percent(success, total):
    return (success / total) * 100 if total else 0

def format_validation_result(result):
    """Formata resultado de validação individual"""
    status_icon = "✅" if result.get('passed', False) else "❌"
    return f"{status_icon} {result.get('message', 'Sem mensagem')}"

def format_summary(total, passed, failed):
    """Formata resumo das validações"""
    success_rate = percent(passed, total)
    return f"📊 Total: {total} | ✅ Passou: {passed} | ❌ Falhou: {failed} | 📈 Taxa: {success_rate:.1f}%"