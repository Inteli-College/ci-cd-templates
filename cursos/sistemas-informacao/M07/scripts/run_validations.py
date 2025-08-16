from checks import docs, readme, assets, source
import json

def main():
    results = []
    results += docs.run_all()
    results += readme.run_all()
    results += assets.run_all()
    results += source.run_all()

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()