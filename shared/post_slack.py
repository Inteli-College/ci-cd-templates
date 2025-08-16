# Utilitário para postar no Slack
import os
import json
import yaml
import requests
from utils.slack_format import format_message

def load_validation_results():
    """Carrega resultados das validações"""
    # Primeiro tenta carregar do arquivo de resultados (sistema antigo)
    results_file = os.environ.get("RESULTS_FILE", "results.json")
    if os.path.exists(results_file):
        with open(results_file) as f:
            return json.load(f)
    
    # Se não existir, simula resultado baseado no status do workflow
    # No sistema novo, os resultados são enviados via exit code
    return {
        "summary": "Validações executadas via sistema configurável",
        "status": "completed",
        "details": "Verifique os logs do workflow para detalhes"
    }

def should_send_notification():
    """Verifica se deve enviar notificação baseado na configuração"""
    config_path = os.environ.get("VALIDATION_CONFIG")
    if not config_path or not os.path.exists(config_path):
        return True  # Default: sempre envia se não há configuração
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            return config.get('notification', {}).get('slack', {}).get('enabled', True)
    except:
        return True  # Em caso de erro, envia por segurança

def main():
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("⚠️ SLACK_WEBHOOK_URL não configurada, pulando notificação")
        return
    
    if not should_send_notification():
        print("ℹ️ Notificações do Slack desabilitadas na configuração")
        return
    
    try:
        results = load_validation_results()
        payload = format_message(results)
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Notificação enviada para o Slack com sucesso")
        else:
            print(f"❌ Erro ao enviar notificação: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao enviar notificação para o Slack: {e}")

if __name__ == "__main__":
    main()