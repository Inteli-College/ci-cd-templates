import os, sys, requests
from datetime import datetime, timedelta, timezone

def main():
    url = os.environ["DATE_SOURCE_URL"]
    data = requests.get(url).json()

    # Ajuste para UTC-3
    tz_brt = timezone(timedelta(hours=-3))
    hoje_local = datetime.now(tz_brt).strftime("%Y-%m-%d")

    if hoje_local not in data.get("datas_avaliacao", []):
        print(f"[INFO] {hoje_local} não é data de avaliação. Encerrando.")
        sys.exit(0)

    print(f"[INFO] {hoje_local} é data de avaliação. Continuando.")

if __name__ == "__main__":
    main()