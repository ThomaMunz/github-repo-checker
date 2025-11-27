import requests
import json
import os
from datetime import datetime

def check_repo_status(owner: str, repo: str) -> dict:
    """
    Проверяет статус GitHub-репозитория через API
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "exists": True,
            "private": data.get("private", False),
            "updated_at": data.get("updated_at"),
            "stars": data.get("stargazers_count", 0),
            "language": data.get("language") or "Not specified"
        }
    elif response.status_code == 404:
        return {"exists": False}
    else:
        raise Exception(f"GitHub API error: {response.status_code}")

def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Создаём шаблон
        config = {"owner": "ThomaMunz", "repo": "test-repo"}
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print("⚠️  Создан config.json — заполните его!")
        return config

if __name__ == "__main__":
    config = load_config()
    owner = config["owner"]
    repo = config["repo"]
    
    try:
        status = check_repo_status(owner, repo)
        print(f"\n🔍 Проверка репозитория: {owner}/{repo}")
        print(f"Дата/время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        if not status["exists"]:
            print("❌ Репозиторий не найден (404). Возможно, он приватный или удалён.")
        else:
            print(f"✅ Репозиторий существует")
            print(f"   Приватный: {'Да' if status['private'] else 'Нет'}")
            print(f"   Последнее обновление: {status['updated_at']}")
            print(f"   Язык: {status['language']}")
            print(f"   ⭐ Звёзд: {status['stars']}")
            
    except Exception as e:
        print(f"Ошибка: {e}")
