def format_message(results):
    """Formata mensagem para o Slack baseado no formato dos resultados"""
    
    # Verifica se é o formato novo (com summary, status, details)
    if isinstance(results, dict) and 'summary' in results:
        status_emoji = "✅" if results.get('status') == 'success' else "❌"
        config_name = results.get('config_name', 'Validação')
        config_description = results.get('config_description', '')
        success_rate = results.get('success_rate', 0)
        summary_stats = results.get('summary_stats', {})
        
        # Cabeçalho principal
        header_text = f"{status_emoji} **{config_name}**"
        if config_description:
            header_text += f"\n_{config_description}_"
        
        # Se temos relatório detalhado, usamos ele
        if 'detailed_report' in results:
            # Limita o relatório para não exceder limite do Slack
            detailed_report = results['detailed_report']
            if len(detailed_report) > 2500:  # Slack tem limite de ~3000 chars por attachment
                # Pega só o resumo e alguns detalhes
                lines = detailed_report.split('\n')
                summary_lines = []
                details_lines = []
                in_details = False
                
                for line in lines:
                    if "RESUMO DAS VALIDAÇÕES" in line or "📊" in line:
                        in_details = False
                    elif "DETALHES" in line or "📋" in line:
                        in_details = True
                        details_lines.append(line)
                        continue
                    
                    if not in_details and ("Total:" in line or "✅" in line or "❌" in line or "📈" in line or "=" in line):
                        summary_lines.append(line)
                    elif in_details and len(details_lines) < 10:  # Limita detalhes
                        details_lines.append(line)
                
                report_text = "\n".join(summary_lines + ["\n"] + details_lines[:10])
                if len(details_lines) > 10:
                    report_text += f"\n... e mais {len(details_lines) - 10} itens (veja logs do workflow)"
            else:
                report_text = detailed_report
            
            return {
                "text": header_text,
                "attachments": [
                    {
                        "title": f"📊 Relatório Completo",
                        "text": f"```\n{report_text}\n```",
                        "color": "good" if results.get('status') == 'success' else "danger",
                        "mrkdwn_in": ["text"]
                    }
                ]
            }
        
        # Fallback se não tiver relatório detalhado
        else:
            return {
                "text": header_text,
                "attachments": [
                    {
                        "title": "📈 Resumo da Validação",
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