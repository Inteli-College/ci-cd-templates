# Utilitário para postar no Slack
import os, json, requests
from utils.slack_format import format_message

def main():
    results_file = os.environ.get("RESULTS_FILE", "results.json")
    with open(results_file) as f:
        results = json.load(f)
    payload = format_message(results)
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    requests.post(webhook_url, json=payload)

if __name__ == "__main__":
    main()